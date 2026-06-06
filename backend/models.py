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
    flight: dict
    hotel: dict
    weather: dict
    activities: dict
    budget_breakdown: dict
    itinerary: str
    recommendation: str


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

class WeatherResult(BaseModel):
    condition: str
    average_temp_celsius: float
    humidity_percent: int
    travel_tip: str


class ActivityResult(BaseModel):
    day_wise_plan: list[dict]
    must_see: list[str]
    estimated_activity_cost: int


class BudgetResult(BaseModel):
    flight_cost: int
    hotel_cost: int
    activity_cost: int
    food_estimate: int
    total_estimated: int
    remaining_budget: int
    is_within_budget: bool
    recommendation: str