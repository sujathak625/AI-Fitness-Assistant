import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GOAL_FILE = os.path.join(BASE_DIR, "data", "goals.json")


# -----------------------------------------
# Ensure file exists
# -----------------------------------------
def _ensure_goal_file():
    if not os.path.exists(os.path.join(BASE_DIR, "data")):
        os.makedirs(os.path.join(BASE_DIR, "data"))

    if not os.path.exists(GOAL_FILE):
        with open(GOAL_FILE, "w") as f:
            json.dump({"goal": "fat_loss"}, f)   # default goal


# -----------------------------------------
# Load user goal
# -----------------------------------------
def get_user_goal():
    _ensure_goal_file()
    try:
        with open(GOAL_FILE, "r") as f:
            data = json.load(f)
            return data.get("goal", "fat_loss")
    except:
        return "fat_loss"   # default fallback


# -----------------------------------------
# Save/update user goal
# -----------------------------------------
def set_user_goal(goal: str):
    _ensure_goal_file()
    valid_goals = ["fat_loss", "muscle_gain", "maintenance", "endurance"]

    if goal not in valid_goals:
        return False

    with open(GOAL_FILE, "w") as f:
        json.dump({"goal": goal}, f, indent=2)

    return True


# -----------------------------------------
# Detect goal from message
# -----------------------------------------
def detect_goal_change(message: str):
    msg = message.lower()

    # Fat loss
    if any(k in msg for k in ["lose weight", "fat loss", "reduce weight", "burn fat"]):
        set_user_goal("fat_loss")
        return "fat_loss"

    # Muscle gain
    if any(k in msg for k in ["gain muscle", "build muscle", "bulk up", "strength"]):
        set_user_goal("muscle_gain")
        return "muscle_gain"

    # Maintenance
    if any(k in msg for k in ["maintain weight", "stay fit", "general fitness"]):
        set_user_goal("maintenance")
        return "maintenance"

    # Endurance
    if any(k in msg for k in ["run", "running", "cardio", "endurance"]):
        set_user_goal("endurance")
        return "endurance"

    return None  # no goal update
