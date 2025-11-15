import requests
from ai_dashboard.config import CHAT_SERVICE_URL

def chat(message):
    return requests.post(f"{CHAT_SERVICE_URL}/chat/respond", json={"message": message}).json()
