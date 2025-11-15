import requests
from ai_dashboard.config import IOT_SERVICE_URL

def get_status():
    return requests.get(f"{IOT_SERVICE_URL}/iot/status").json()

def get_recommendation():
    return requests.get(f"{IOT_SERVICE_URL}/iot/recommendation").json()
