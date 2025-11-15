import requests
from ai_dashboard.config import DIET_SERVICE_URL

def get_diet_plan(data):
    return requests.post(f"{DIET_SERVICE_URL}/diet/plan", json=data).json()

def get_grocery_list(meal_plan):
    return requests.post(
        f"{DIET_SERVICE_URL}/diet/grocery-list",
        json={"meal_plan": meal_plan}
    ).json()
