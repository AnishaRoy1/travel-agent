from pydantic import BaseModel


# --- Request/Response ---

class TripRequest(BaseModel):
    source: str
    destination: str
    days: int
    budget: int


class TripResponse(BaseModel):
    destination: str
    days: int
    budget: int
    itinerary: str
    flight: dict
    hotel: dict


# --- Agent output models ---

class FlightResult(BaseModel):
    airline: str
    estimated_cost: int
    duration_hours: float
    stops: int
    notes: str


class HotelResult(BaseModel):
    name: str
    location: str
    estimated_cost_per_night: int
    total_cost: int
    rating: float
    notes: str