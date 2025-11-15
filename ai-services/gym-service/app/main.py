from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List, Optional
import math
import json
import os

app = FastAPI(title="Gym Recommender & Planner")

# ---------------------------------------------------------
# Load gyms from JSON file
# ---------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GYM_FILE = os.path.join(BASE_DIR, "data", "gyms.json")

with open(GYM_FILE, "r") as f:
    GYMS = json.load(f)["gyms"]


# ---------------------------------------------------------
# Haversine distance
# ---------------------------------------------------------
def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)

    a = (math.sin(d_lat / 2) ** 2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(d_lon / 2) ** 2)

    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


# ---------------------------------------------------------
# Pydantic Models
# ---------------------------------------------------------
class GymOut(BaseModel):
    id: str
    name: str
    city: str
    lat: float
    lon: float
    distance_km: float
    price_tier: str
    membership_price: int
    amenities: List[str]
    opening_hours: str
    morning_classes: bool
    goals_supported: List[str]
    rating: float


class PlanRequest(BaseModel):
    goal: str
    level: Optional[str] = "beginner"
    days_per_week: Optional[int] = 3


class PlanOut(BaseModel):
    goal: str
    level: str
    days_per_week: int
    weekly_plan: dict


# ---------------------------------------------------------
# Health
# ---------------------------------------------------------
@app.get("/health")
async def health():
    return {"status": "ok", "service": "gym-recommender"}


# ---------------------------------------------------------
# 1️⃣ Gym Finder (Supports radius, city, budget, goal, morning-only)
# ---------------------------------------------------------
@app.get("/gyms", response_model=List[GymOut])
async def find_gyms(
        lat: float,
        lon: float,
        city: Optional[str] = None,
        goal: Optional[str] = None,
        radius_km: float = 5.0,
        budget: Optional[str] = None,
        morning_only: bool = False,
        max_results: int = 10
):

    results = []

    for gym in GYMS:

        # Filter by city
        if city and gym["city"].lower() != city.lower():
            continue

        # Budget filter
        if budget and gym["price_tier"] != budget:
            continue

        # Morning classes filter
        if morning_only and not gym["morning_classes"]:
            continue

        # Goal filter
        if goal and goal.lower() not in [g.lower() for g in gym["goals_supported"]]:
            continue

        # Distance filter (if radius_km is 0, skip filtering)
        d = haversine_km(lat, lon, gym["lat"], gym["lon"])
        if radius_km > 0 and d > radius_km:
            continue

        gym_copy = gym.copy()
        gym_copy["distance_km"] = round(d, 2)
        results.append(gym_copy)

    results.sort(key=lambda x: (x["distance_km"], -x["rating"]))

    return results[:max_results]


# ---------------------------------------------------------
# 2️⃣ Weekly Workout Planner
# ---------------------------------------------------------
@app.post("/plan", response_model=PlanOut)
async def generate_plan(req: PlanRequest):

    goal = req.goal.lower()
    level = req.level.lower()
    dpw = max(1, min(7, req.days_per_week))

    def block(goal, level):
        if goal == "fat_loss":
            if level == "beginner":
                return ["10 min warm-up", "15 min walking/HIIT", "10 min core"]
            else:
                return ["10 min warm-up", "30 min HIIT", "10 min stretch"]

        if goal == "muscle_gain":
            return ["Strength Training 45–60 min", "Progressive overload"]

        if goal == "flexibility":
            return ["Yoga / Mobility 40 min"]

        return ["Cardio 20 min", "Strength 20 min", "Stretch 10 min"]

    week = {f"day_{i}": block(goal, level) for i in range(1, dpw + 1)}

    return PlanOut(goal=goal, level=level, days_per_week=dpw, weekly_plan=week)


# ---------------------------------------------------------
# 3️⃣ Full Recommender
# ---------------------------------------------------------
@app.post("/recommend")
async def recommend(
        lat: float,
        lon: float,
        city: str,
        goal: str = "general_fitness",
        level: str = "beginner",
        days_per_week: int = 3
):
    gyms = await find_gyms(lat=lat, lon=lon, city=city, goal=goal, radius_km=5)
    plan = await generate_plan(PlanRequest(goal=goal, level=level, days_per_week=days_per_week))

    return {"gyms": gyms, "plan": plan}
