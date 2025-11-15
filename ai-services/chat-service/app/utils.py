# utils.py (helpers)
import re
import requests
from typing import Optional, List

from .memory import get_user_profile

CHAT_DEFAULTS = {}

def safe_text(s: str) -> str:
    return (s or "").strip()

def fuzzy_contains(text: str, patterns: List[str]) -> bool:
    t = text.lower()
    for p in patterns:
        if p in t:
            return True
    return False


# Try to call gym service; returns list or None
def call_gym_service(city: Optional[str] = None):
    from ai_dashboard.config import GYM_SERVICE_URL
    try:
        params = {}
        if city:
            params["city"] = city
        # attempt to call gyms endpoint
        res = requests.get(f"{GYM_SERVICE_URL}/gyms", params=params, timeout=3)
        if res.status_code == 200:
            return res.json()
    except Exception:
        pass
    # fallback sample list
    sample = [
        {"id": "gym_101", "name": "CoreFit", "city": city or "Bangalore", "price_tier": "mid", "distance_km": 1.2, "rating": 4.4},
        {"id": "gym_102", "name": "Urban Strength", "city": city or "Bangalore", "price_tier": "high", "distance_km": 2.0, "rating": 4.7},
        {"id": "gym_103", "name": "Neighborhood Fitness", "city": city or "Bangalore", "price_tier": "low", "distance_km": 0.8, "rating": 4.1}
    ]
    return sample
