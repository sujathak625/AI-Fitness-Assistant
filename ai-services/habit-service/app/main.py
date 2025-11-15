from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import json
import os

app = FastAPI(title="Habit Tracker Service")

DATA_FILE = "habit_data.json"

# --------------------------------------------------
# Ensure file exists
# --------------------------------------------------
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({"logs": []}, f)


# --------------------------------------------------
# Helper: Load + Save
# --------------------------------------------------
def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


# --------------------------------------------------
# Pydantic Model
# --------------------------------------------------
class HabitLog(BaseModel):
    habit: str
    status: str   # Completed / Skipped / Partial


# --------------------------------------------------
# API Endpoints
# --------------------------------------------------
@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/habits/logs")
async def get_logs():
    data = load_data()
    return {"logs": data.get("logs", [])}

@app.post("/habits/log")
async def add_log(entry: HabitLog):
    data = load_data()
    logs = data.get("logs", [])

    logs.append({
        "habit": entry.habit,
        "status": entry.status,
        "date": datetime.now().isoformat()
    })

    data["logs"] = logs
    save_data(data)

    return {"success": True, "message": "Habit log saved!", "log_count": len(logs)}
