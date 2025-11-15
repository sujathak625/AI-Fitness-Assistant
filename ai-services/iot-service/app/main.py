# ai-services/iot-service/app/main.py
from fastapi import FastAPI
from pydantic import BaseModel
import threading
import time
import random

app = FastAPI(title="Smart Gym IoT Assistant (Streaming)")


# =========================================================
# 🔐 THREAD-SAFE SENSOR STATE
# =========================================================
state_lock = threading.Lock()

sensor_data = {
    "machine": None,
    "heart_rate": 0,
    "speed": 0.0,
    "reps": 0,
    "fatigue": 0.0,
    "ai_feedback": "Idle",
    "total_calories": 0.0,
    "session_active": False,
    "session_started_at": None,
    "session_elapsed": 0
}

# =========================================================
# 🔧 MACHINE PROFILES (HR range, speed range, MET values)
# =========================================================
MACHINE_PROFILES = {
    "treadmill": {"hr_min": 110, "hr_max": 165, "speed_min": 4.0, "speed_max": 12.0, "met": 7.0},
    "cycling":   {"hr_min": 100, "hr_max": 155, "speed_min": 20.0, "speed_max": 80.0, "met": 6.0},
    "rowing":    {"hr_min": 110, "hr_max": 170, "speed_min": 20.0, "speed_max": 40.0, "met": 8.0},
    "elliptical":{"hr_min": 95,  "hr_max": 150, "speed_min": 3.0, "speed_max": 10.0, "met": 5.5},
    "dumbbells": {"hr_min": 80,  "hr_max": 140, "speed_min": 0.0, "speed_max": 0.0,  "met": 4.5},
}

VIRTUAL_WEIGHT_KG = 70.0  # calorie formula body weight assumption

# Streaming thread control
_stream_thread = None
_stream_stop_flag = threading.Event()


# =========================================================
# 🤖 AI LOGIC FOR FEEDBACK + FATIGUE SCORE
# =========================================================
def evaluate_ai_logic():
    with state_lock:
        hr = sensor_data["heart_rate"]
        speed = sensor_data["speed"]
        reps = sensor_data["reps"]

    feedback = []

    # Heart rate insights
    if hr > 180:
        feedback.append("⚠️ Danger: HR very high!")
    elif hr > 160:
        feedback.append("🔥 High HR — slow down.")
    elif hr > 120:
        feedback.append("💪 Good workout zone.")
    else:
        feedback.append("❤️ Light or warm-up.")

    # Speed insights
    if speed > 0:
        if speed > 12:
            feedback.append("⚠️ Very fast speed.")
        elif speed > 8:
            feedback.append("🏃 Good pace.")
        else:
            feedback.append("🚶 Moderate pace.")

    # Rep insights
    if reps > 20:
        feedback.append("🔥 High reps — fatigue likely.")
    elif reps > 10:
        feedback.append("💪 Good reps.")
    elif reps > 0:
        feedback.append("✨ Warm-up reps.")

    with state_lock:
        sensor_data["fatigue"] = round(min(1.0, (hr / 180) * 0.6 + (speed / 12) * 0.4), 2)
        sensor_data["ai_feedback"] = " | ".join(feedback)


# =========================================================
# 🔥 CALORIE CALC (PER SECOND)
# =========================================================
def calories_per_second(met_value):
    # Calories/min = MET × 3.5 × weight(kg) / 200
    cal_per_min = met_value * 3.5 * VIRTUAL_WEIGHT_KG / 200.0
    return cal_per_min / 60.0


# =========================================================
# 🧵 BACKGROUND STREAMING WORKER
# =========================================================
def _stream_worker(machine_name: str, duration_seconds: int = 60):
    profile = MACHINE_PROFILES[machine_name]
    met_value = profile["met"]

    start_ts = time.time()

    with state_lock:
        sensor_data["session_active"] = True
        sensor_data["session_started_at"] = start_ts
        sensor_data["session_elapsed"] = 0
        sensor_data["total_calories"] = 0.0
        sensor_data["machine"] = machine_name
        sensor_data["reps"] = 0

    _stream_stop_flag.clear()

    # Main streaming loop
    while True:
        elapsed = int(time.time() - start_ts)

        if elapsed >= duration_seconds or _stream_stop_flag.is_set():
            break

        # Random realistic measurements
        hr = random.randint(profile["hr_min"], profile["hr_max"])
        spd = round(random.uniform(profile["speed_min"], profile["speed_max"]), 1)

        # Rep behavior per machine
        if machine_name in ("treadmill", "rowing"):
            rep_added = random.randint(1, 4)
            with state_lock:
                sensor_data["reps"] += rep_added
        else:
            with state_lock:
                sensor_data["reps"] = random.randint(0, 30)

        # Save new metrics
        with state_lock:
            sensor_data["heart_rate"] = hr
            sensor_data["speed"] = spd
            sensor_data["session_elapsed"] = elapsed

        evaluate_ai_logic()

        # 🔥 accumulate calories
        with state_lock:
            sensor_data["total_calories"] += calories_per_second(met_value)

        time.sleep(1)

    # End session cleanly
    with state_lock:
        sensor_data["session_active"] = False


# =========================================================
# 📡 FASTAPI MODELS
# =========================================================
class IoTStatus(BaseModel):
    machine: str | None
    heart_rate: int
    speed: float
    reps: int
    fatigue: float
    ai_feedback: str
    total_calories: float
    session_active: bool
    session_elapsed: int


# =========================================================
# 📍 ENDPOINTS
# =========================================================
@app.get("/health")
async def health():
    return {"status": "ok", "service": "iot-service"}


@app.get("/iot/status")
async def iot_status():
    with state_lock:
        return {
            "machine": sensor_data["machine"],
            "heart_rate": sensor_data["heart_rate"],
            "speed": sensor_data["speed"],
            "reps": sensor_data["reps"],
            "fatigue": sensor_data["fatigue"],
            "ai_feedback": sensor_data["ai_feedback"],
            "total_calories": round(sensor_data["total_calories"], 3),
            "session_active": sensor_data["session_active"],
            "session_elapsed": sensor_data["session_elapsed"]
        }


@app.get("/iot/demo")
async def iot_demo():
    """One-shot demo reading (NOT streaming)."""
    profile = MACHINE_PROFILES["treadmill"]

    with state_lock:
        sensor_data["heart_rate"] = random.randint(profile["hr_min"], profile["hr_max"])
        sensor_data["speed"] = round(random.uniform(profile["speed_min"], profile["speed_max"]), 1)
        sensor_data["reps"] = random.randint(0, 20)

    evaluate_ai_logic()
    return await iot_status()


@app.get("/iot/set-machine/{machine_name}")
async def set_machine(machine_name: str):
    if machine_name not in MACHINE_PROFILES:
        return {"status": "error", "message": f"Unknown machine {machine_name}"}

    with state_lock:
        sensor_data["machine"] = machine_name
        sensor_data["total_calories"] = 0.0
        sensor_data["session_active"] = False
        sensor_data["session_elapsed"] = 0
        sensor_data["reps"] = 0

    return {"status": "ok", "machine": machine_name}


@app.get("/iot/stream/start/{machine_name}")
async def stream_start(machine_name: str, duration: int = 60):
    """Start streaming in background (non-blocking)."""
    global _stream_thread, _stream_stop_flag

    if machine_name not in MACHINE_PROFILES:
        return {"status": "error", "message": "unknown machine"}

    with state_lock:
        if sensor_data["session_active"]:
            return {"status": "already_running"}

    _stream_stop_flag.clear()
    _stream_thread = threading.Thread(
        target=_stream_worker, args=(machine_name, duration), daemon=True
    )
    _stream_thread.start()

    return {"status": "started", "machine": machine_name, "duration": duration}


@app.get("/iot/stream/stop")
async def stream_stop():
    _stream_stop_flag.set()
    return {"status": "stopping"}


@app.get("/iot/reset")
async def reset():
    with state_lock:
        sensor_data.update({
            "machine": None,
            "heart_rate": 0,
            "speed": 0.0,
            "reps": 0,
            "fatigue": 0.0,
            "ai_feedback": "Idle",
            "total_calories": 0.0,
            "session_active": False,
            "session_started_at": None,
            "session_elapsed": 0
        })
    return {"status": "reset"}
