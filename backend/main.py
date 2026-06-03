import asyncio
from fastapi import FastAPI, HTTPException
from google import genai
from config import GEMINI_API_KEY
from models import TripRequest, TripResponse
from agents.flight_agent import flight_agent
from agents.hotel_agent import hotel_agent

client = genai.Client(api_key=GEMINI_API_KEY)

app = FastAPI()


async def generate_summary(trip: TripRequest, flight: dict, hotel: dict) -> str:
    prompt = f"""
    You are a travel planning assistant.
    
    Trip details:
    - From: {trip.source} to {trip.destination}
    - Duration: {trip.days} days
    - Budget: ₹{trip.budget}
    
    Flight booked:
    - Airline: {flight['airline']}
    - Cost: ₹{flight['estimated_cost']}
    - Duration: {flight['duration_hours']} hours
    
    Hotel booked:
    - Name: {hotel['name']}
    - Location: {hotel['location']}
    - Total cost: ₹{hotel['total_cost']}
    
    Write a brief 3-4 line travel summary and one key tip for this trip.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text


@app.get("/")
def root():
    return {"message": "Travel Agent API is running"}

@app.get("/list-models")
def list_models():
    models = client.models.list()
    return {"models": [m.name for m in models]}


@app.post("/plan-trip", response_model=TripResponse)
async def plan_trip(trip: TripRequest):
    if trip.days < 1 or trip.days > 30:
        raise HTTPException(status_code=400, detail="Days must be between 1 and 30")

    if trip.budget < 5000:
        raise HTTPException(status_code=400, detail="Budget too low — minimum ₹5000")

    # Run both agents in parallel
    flight_result, hotel_result = await asyncio.gather(
        flight_agent(trip.source, trip.destination),
        hotel_agent(trip.destination, trip.days)
    )

    # Generate summary using both results
    summary = await generate_summary(
        trip,
        flight_result.model_dump(),
        hotel_result.model_dump()
    )

    return TripResponse(
        destination=trip.destination,
        days=trip.days,
        budget=trip.budget,
        itinerary=summary,
        flight=flight_result.model_dump(),
        hotel=hotel_result.model_dump()
    )