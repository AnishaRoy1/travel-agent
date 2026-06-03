import json
from google import genai
from config import GEMINI_API_KEY
from models import FlightResult

client = genai.Client(api_key=GEMINI_API_KEY)


async def flight_agent(source: str, destination: str) -> FlightResult:
    prompt = f"""
    You are a flight data agent. Your job is to estimate flight options.
    
    Route: {source} to {destination}
    
    Return ONLY a valid JSON object with exactly these fields:
    {{
        "airline": "most likely airline for this route",
        "estimated_cost": cost in rupees as integer,
        "duration_hours": flight duration as decimal number,
        "stops": number of stops as integer,
        "notes": "one useful tip about this flight"
    }}
    
    No explanation. No markdown. No code blocks. Just the raw JSON object.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    raw = response.text.strip()

    # Strip markdown code blocks if Gemini adds them anyway
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    data = json.loads(raw)
    return FlightResult(**data)