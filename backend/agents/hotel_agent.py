import json
from google import genai
from config import GEMINI_API_KEY
from models import HotelResult

client = genai.Client(api_key=GEMINI_API_KEY)


async def hotel_agent(destination: str, days: int) -> HotelResult:
    prompt = f"""
    You are a hotel recommendation agent.
    
    Destination: {destination}
    Duration: {days} nights
    
    Return ONLY a valid JSON object with exactly these fields:
    {{
        "name": "a real or realistic hotel name",
        "location": "neighbourhood or area name",
        "estimated_cost_per_night": cost per night in rupees as integer,
        "total_cost": total cost for all nights in rupees as integer,
        "rating": rating out of 5 as decimal,
        "notes": "one useful tip about this hotel or area"
    }}
    
    No explanation. No markdown. No code blocks. Just the raw JSON object.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    raw = response.text.strip()

    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    data = json.loads(raw)
    return HotelResult(**data)