# -----------------------------
# Centralized Configuration File
# -----------------------------

POSE_SERVICE_URL = "http://127.0.0.1:8000"
DIET_SERVICE_URL = "http://127.0.0.1:8100"
HABIT_SERVICE_URL = "http://127.0.0.1:8200"
CHAT_SERVICE_URL = "http://127.0.0.1:8300"
GYM_SERVICE_URL = "http://127.0.0.1:8600"
IOT_SERVICE_URL = "http://127.0.0.1:8500"

# -----------------------------
# Optional: Deployment Switch
# -----------------------------
ENV = "LOCAL"   # change to PROD during deployment

if ENV == "PROD":
    POSE_SERVICE_URL = "https://your-domain.com/pose"
    DIET_SERVICE_URL = "https://your-domain.com/diet"
    HABIT_SERVICE_URL = "https://your-domain.com/habit"
    CHAT_SERVICE_URL = "https://your-domain.com/chat"
    GYM_SERVICE_URL = "https://your-domain.com/gym"
    IOT_SERVICE_URL = "https://your-domain.com/iot"
