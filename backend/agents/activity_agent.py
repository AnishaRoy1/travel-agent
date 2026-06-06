import json
from google import genai
from config import GEMINI_API_KEY
from models import ActivityResult

client = genai.Client(api_key=GEMINI_API_KEY)


async def activity_agent(destination: str, days: int) -> ActivityResult:
    prompt = f"""
    You are a travel activity planner.
    
    Destination: {destination}
    Duration: {days} days
    
    Return ONLY a valid JSON object with exactly these fields:
    {{
        "day_wise_plan": [
            {{
                "day": 1,
                "morning": "activity description",
                "afternoon": "activity description",
                "evening": "activity description"
            }}
        ],
        "must_see": ["attraction 1", "attraction 2", "attraction 3"],
        "estimated_activity_cost": total cost in rupees for all activities as integer
    }}
    
    Create one entry in day_wise_plan for each of the {days} days.
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
    return ActivityResult(**data)