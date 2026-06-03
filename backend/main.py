from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai
from config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

app = FastAPI()


class TripRequest(BaseModel):
    source: str
    destination: str
    days: int
    budget: int


class TripResponse(BaseModel):
    itinerary: str
    destination: str
    days: int
    budget: int


def generate_itinerary(trip: TripRequest) -> str:
    prompt = f"""
    You are a travel planning assistant.
    
    Plan a {trip.days}-day trip from {trip.source} to {trip.destination}.
    The total budget is ₹{trip.budget}.
    
    Return a detailed day-by-day itinerary including:
    - What to do each day
    - Rough cost estimates
    - Travel tips for the destination
    
    Keep it practical and specific.
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
def plan_trip(trip: TripRequest):
    if trip.days < 1 or trip.days > 30:
        raise HTTPException(status_code=400, detail="Days must be between 1 and 30")

    if trip.budget < 5000:
        raise HTTPException(status_code=400, detail="Budget too low — minimum ₹5000")

    itinerary = generate_itinerary(trip)

    return TripResponse(
        itinerary=itinerary,
        destination=trip.destination,
        days=trip.days,
        budget=trip.budget
    )