from typing import List

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

API_KEY = "ak_jzin7znrdmgcywhr95594m12"
EMAIL = "24f3004140@ds.study.iitm.ac.in"

app = FastAPI(
    title="Analytics API"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root endpoint (helps verify deployment)
@app.get("/")
def home():
    return {"message": "Analytics API is running!"}


class Event(BaseModel):
    user: str
    amount: float
    ts: int


class AnalyticsRequest(BaseModel):
    events: List[Event]


@app.post("/analytics")
def analytics(
    request: AnalyticsRequest,
    x_api_key: str | None = Header(default=None)
):
    # Authentication
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    total_events = len(request.events)

    unique_users = len({event.user for event in request.events})

    revenue = sum(event.amount for event in request.events if event.amount > 0)

    user_totals = {}
    for event in request.events:
        if event.amount > 0:
            user_totals[event.user] = user_totals.get(event.user, 0) + event.amount

    top_user = max(user_totals, key=user_totals.get) if user_totals else ""

    return {
        "email": EMAIL,
        "total_events": total_events,
        "unique_users": unique_users,
        "revenue": revenue,
        "top_user": top_user
    }