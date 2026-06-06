import asyncio
from fastapi import FastAPI, HTTPException
from google import genai
from config import GEMINI_API_KEY
from models import TripRequest, TripResponse
from agents.flight_agent import flight_agent
from agents.hotel_agent import hotel_agent
from agents.weather_agent import weather_agent
from agents.activity_agent import activity_agent
from agents.budget_agent import budget_agent
from fastapi.middleware.cors import CORSMiddleware

client = genai.Client(api_key=GEMINI_API_KEY)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://travel-agent-snowy-kappa.vercel.app",
        "https://travel-agent-prod.up.railway.app"
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)


async def generate_final_itinerary(
    trip: TripRequest,
    flight: dict,
    hotel: dict,
    weather: dict,
    activities: dict,
    budget: dict
) -> str:
    prompt = f"""
    You are a travel planning assistant. Generate a friendly, 
    detailed final travel itinerary based on the data below.
    
    Trip: {trip.days} days from {trip.source} to {trip.destination}
    Budget: ₹{trip.budget}
    
    Flight: {flight['airline']}, ₹{flight['estimated_cost']}, 
            {flight['duration_hours']} hours, {flight['stops']} stop(s)
    
    Hotel: {hotel['name']} in {hotel['location']}, 
           ₹{hotel['estimated_cost_per_night']}/night, rated {hotel['rating']}/5
    
    Weather: {weather['condition']}, {weather['average_temp_celsius']}°C, 
             humidity {weather['humidity_percent']}%
    
    Activities planned: {activities['must_see']}
    
    Budget status: {'Within budget ✓' if budget['is_within_budget'] else 'Over budget ✗'}
    Total estimated cost: ₹{budget['total_estimated']}
    
    Write a warm, helpful 5-6 line itinerary summary covering:
    - Travel and accommodation highlights
    - Weather advice
    - Top activities to prioritize
    - Budget situation
    Keep it practical and encouraging.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text


@app.get("/")
def root():
    return {"message": "Travel Agent API is running"}


@app.post("/plan-trip", response_model=TripResponse)
async def plan_trip(trip: TripRequest):
    if trip.days < 1 or trip.days > 30:
        raise HTTPException(
            status_code=400,
            detail="Days must be between 1 and 30"
        )

    if trip.budget < 5000:
        raise HTTPException(
            status_code=400,
            detail="Budget too low — minimum ₹5000"
        )

    # Run 4 agents in parallel
    flight_result, hotel_result, weather_result, activity_result = await asyncio.gather(
        flight_agent(trip.source, trip.destination),
        hotel_agent(trip.destination, trip.days),
        weather_agent(trip.destination, trip.days),
        activity_agent(trip.destination, trip.days)
    )

    # Budget agent is pure math — no API call needed
    budget_result = budget_agent(
        trip_budget=trip.budget,
        flight=flight_result,
        hotel=hotel_result,
        activity=activity_result,
        days=trip.days
    )

    # Final LLM summary using all agent outputs
    itinerary = await generate_final_itinerary(
        trip=trip,
        flight=flight_result.model_dump(),
        hotel=hotel_result.model_dump(),
        weather=weather_result.model_dump(),
        activities=activity_result.model_dump(),
        budget=budget_result.model_dump()
    )

    return TripResponse(
        destination=trip.destination,
        days=trip.days,
        budget=trip.budget,
        flight=flight_result.model_dump(),
        hotel=hotel_result.model_dump(),
        weather=weather_result.model_dump(),
        activities=activity_result.model_dump(),
        budget_breakdown=budget_result.model_dump(),
        itinerary=itinerary,
        recommendation=budget_result.recommendation
    )