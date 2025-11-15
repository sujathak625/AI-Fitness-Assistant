import requests
from ai_dashboard.config import HABIT_SERVICE_URL

def habit_status():
    return requests.get(f"{HABIT_SERVICE_URL}/habit/status").json()

def habit_predict(user_id):
    return requests.get(f"{HABIT_SERVICE_URL}/habit/predict?user_id={user_id}").json()
