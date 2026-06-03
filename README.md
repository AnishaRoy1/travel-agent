# ✈️ Travel Agent

An intelligent AI-powered travel planning application that uses multiple specialized LLM agents to create personalized trip itineraries. Built with Python async, FastAPI, and Google Gemini API.

## 🎯 Vision

Create a one-stop travel planning assistant that coordinates multiple specialized agents to generate complete trip plans including flights, hotels, activities, weather forecasts, and budget breakdowns—all optimized for your preferences and constraints.

## 📋 Project Status

**Current Phase:** Week 1 — Learning & Foundation (In Progress)
- ✅ Python async fundamentals
- ✅ Pydantic models & data validation
- ✅ FastAPI basics & POST endpoints
- ✅ Gemini API integration
- ✅ Flight & Hotel agents (basic)
- 🚧 Full agent suite coming Week 2

## 🏗️ Architecture

### Backend Stack
- **Framework:** FastAPI (async Python web framework)
- **LLM Provider:** Google Gemini 2.0 Flash
- **Data Validation:** Pydantic
- **Concurrency:** asyncio + asyncio.gather
- **Deployment:** Railway (planned Week 3)

### Agents (Current & Planned)
```
Travel Coordinator (Central)
├── Flight Agent ✅ (current)
├── Hotel Agent ✅ (current)
├── Weather Agent 🚧 (Week 2)
├── Activity Agent 🚧 (Week 2)
└── Budget Agent 🚧 (Week 2)
```

Each agent specializes in one domain and returns structured JSON data. The coordinator runs all agents in parallel using `asyncio.gather()`.

### Frontend (Planned Week 3)
- **Framework:** Next.js (React)
- **Features:** Trip form, results page, budget breakdown
- **Deployment:** Vercel

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- `pip` or `conda`
- Gemini API key (get one free at [ai.google.dev](https://ai.google.dev))

### Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/AnishaRoy1/travel-agent.git
   cd travel-agent/backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   *(If requirements.txt doesn't exist, manually install: `fastapi uvicorn google-genai python-dotenv pydantic`)*

4. **Add your API key**
   ```bash
   echo "GEMINI_API_KEY=your_api_key_here" > .env
   ```

5. **Start the server**
   ```bash
   uvicorn main:app --reload
   ```
   
   API runs at: `http://localhost:8000`

## 📡 API Endpoints

### Health Check
```bash
GET /
```
Response:
```json
{
  "message": "Travel Agent API is running"
}
```

### List Available Models
```bash
GET /list-models
```
Returns all available Gemini models your account can access.

### Plan a Trip
```bash
POST /plan-trip
```

**Request Body:**
```json
{
  "source": "New York",
  "destination": "Tokyo",
  "days": 7,
  "budget": 50000
}
```

**Response:**
```json
{
  "destination": "Tokyo",
  "days": 7,
  "budget": 50000,
  "itinerary": "Your trip summary here...",
  "flight": {
    "airline": "ANA",
    "estimated_cost": 35000,
    "duration_hours": 14.5,
    "stops": 0,
    "notes": "Book early for better rates"
  },
  "hotel": {
    "name": "Hotel Metropolitan Tokyo",
    "location": "Shinjuku",
    "estimated_cost_per_night": 150,
    "total_cost": 1050,
    "rating": 4.5,
    "notes": "Central location with great transport access"
  }
}
```

**Error Responses:**
- `400` — Invalid input (days out of range 1-30, budget < ₹5000)
- `500` — API/LLM error (check Gemini quota)

## 🔧 Usage Examples

### Using cURL
```bash
curl -X POST http://localhost:8000/plan-trip \
  -H "Content-Type: application/json" \
  -d '{
    "source": "Mumbai",
    "destination": "Bali",
    "days": 5,
    "budget": 30000
  }'
```

### Using Python
```python
import httpx
import asyncio

async def plan_trip():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/plan-trip",
            json={
                "source": "Mumbai",
                "destination": "Bali",
                "days": 5,
                "budget": 30000
            }
        )
        return response.json()

result = asyncio.run(plan_trip())
print(result)
```

### Using VS Code REST Client
See `backend/test_requests.http` for pre-made requests.

## 📁 Project Structure

```
travel-agent/
├── backend/
│   ├── main.py                 # FastAPI app + coordinator
│   ├── config.py               # Configuration (API keys)
│   ├── models.py               # Pydantic data models
│   ├── agents/
│   │   ├── flight_agent.py     # Flight search & booking
│   │   ├── hotel_agent.py      # Hotel recommendations
│   │   ├── weather_agent.py    # Weather forecasts (Week 2)
│   │   ├── activity_agent.py   # Activity suggestions (Week 2)
│   │   └── budget_agent.py     # Budget analysis (Week 2)
│   ├── test_requests.http      # API test requests
│   ├── requirements.txt        # Python dependencies
│   └── .env                    # Environment variables (gitignored)
├── frontend/                   # Next.js app (Week 3)
├── README.md                   # This file
└── .gitignore
```

## 📅 Development Roadmap

### ✅ Week 1 — Foundation (In Progress)
- Python async + LLM APIs + FastAPI fundamentals
- Flight & Hotel agents with mock/LLM data
- **Estimated completion:** June 7, 2025

### 🚧 Week 2 — Build All Agents
- Weather agent (OpenWeather API)
- Activity & Budget agents
- Coordinator running all agents in parallel
- End-to-end testing
- **Estimated completion:** June 14, 2025

### 📅 Week 3 — Shipping
- Next.js frontend with trip form
- Results page & itinerary UI
- Budget breakdown component
- Deploy backend (Railway) & frontend (Vercel)
- Final polish & documentation

**Timeline:** 3 weeks, ~40 hrs total

## 🔑 Key Technologies

| Component | Tech | Why? |
|-----------|------|------|
| Backend | FastAPI | Modern, async-first, auto-docs |
| LLM | Google Gemini 2.0 Flash | Fast, free tier, structured output |
| Data | Pydantic | Type-safe validation |
| Async | asyncio | Parallel agent execution |
| Frontend | Next.js | SSR, optimized for production |
| Deployment | Railway + Vercel | Simple, free tier available |

## 🐛 Troubleshooting

### `404 NOT_FOUND — Model not found`
**Fix:** Update the model name in agents. Currently using `gemini-2.0-flash`. Check available models with `GET /list-models`.

### `429 RESOURCE_EXHAUSTED — Quota exceeded`
**Fix:** You've hit the Gemini API free tier limit (~60 requests/day). Either:
- Wait for daily quota reset
- Enable paid tier in [Google AI Studio](https://aistudio.google.com/app/apikey)
- Use a different LLM provider

### `ModuleNotFoundError: No module named 'google'`
**Fix:** Install dependencies: `pip install -r requirements.txt`

### Port 8000 already in use
**Fix:** Use a different port: `uvicorn main:app --port 8001 --reload`

## 📚 Learning Resources

- [Python async/await](https://docs.python.org/3/library/asyncio.html)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Google Gemini API Docs](https://ai.google.dev/gemini-api/docs)
- [Pydantic v2](https://docs.pydantic.dev/)
- [asyncio.gather()](https://docs.python.org/3/library/asyncio-task.html#asyncio.gather)

## 🤝 Contributing

This is a personal learning project but contributions welcome! Feel free to:
- Report bugs in Issues
- Suggest features
- Submit PRs for improvements

## 📄 License

MIT License — Feel free to use this for learning or as a template.

## 👩‍💻 Author

**Anisha Roy**
- GitHub: [@AnishaRoy1](https://github.com/AnishaRoy1)
- Project: Travel Agent (Learning journey)

---

**Built with ❤️ to learn async Python, LLM APIs, and modern web development.**

*Last Updated: June 3, 2025 | Phase: Week 1*
