import requests
from ai_dashboard.config import GYM_SERVICE_URL

def search_gyms(city, goal):
    return requests.get(f"{GYM_SERVICE_URL}/gym/search?city={city}&goal={goal}").json()
