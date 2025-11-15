import re

# ------------------------------------------------------
# USER MEMORY (session-only)
# ------------------------------------------------------
user_profile = {
    "goal": None,
    "diet_pref": None,
    "age": None,
    "weight": None,
    "height": None,
    "gender": None,
    "city": None,
    "gym_timing": None,
    "budget": None,
}

def remember(field, value):
    if value:
        user_profile[field] = value


# ------------------------------------------------------
# MAIN NLP LOGIC
# ------------------------------------------------------
def generate_ai_reply(msg: str):
    msg_low = msg.lower()

    # ---------------------- GREETINGS ----------------------
    if msg_low in ["hi", "hello", "hey", "yo", "hii"]:
        return {"reply": "Hello! I'm your AI fitness assistant. How can I help you today? 😊"}

    # ---------------------- Extract Info -------------------
    age = re.search(r"(\d+)\s*(years|year|yrs)", msg_low)
    weight = re.search(r"(\d+)\s*(kg|kilogram)", msg_low)
    height = re.search(r"(\d+)\s*(cm|centimeter)", msg_low)
    budget = re.search(r"under\s*(\d+)", msg_low)

    if age:
        remember("age", int(age.group(1)))
    if weight:
        remember("weight", int(weight.group(1)))
    if height:
        remember("height", int(height.group(1)))
    if budget:
        remember("budget", int(budget.group(1)))

    # ---------------------- INTENT DETECTION -----------------
    if any(k in msg_low for k in ["diet", "food plan", "meal plan", "nutrition"]):
        return handle_diet_flow(msg_low)

    if any(k in msg_low for k in ["gym", "find a gym", "fitness centre"]):
        return handle_gym_flow(msg_low)

    if any(k in msg_low for k in ["workout", "exercise", "train"]):
        return handle_workout_flow(msg_low)

    # ---------------------- DEFAULT ---------------------------
    return {"reply": "I'm here for **diet**, **gym**, **workout**, or **habit** support. What do you need?"}


# ============================================================
#                       DIET FLOW
# ============================================================
def handle_diet_flow(msg_low):

    # ---- Goal detection ----
    if any(p in msg_low for p in ["lose weight", "weight loss", "fat loss", "reduce weight"]):
        remember("goal", "lose")
    elif any(p in msg_low for p in ["gain weight", "bulk", "build muscle"]):
        remember("goal", "gain")
    elif "maintain" in msg_low:
        remember("goal", "maintain")
    elif "lose" in msg_low:
        remember("goal", "lose")
    elif "gain" in msg_low:
        remember("goal", "gain")

    # ---- Diet preference ----
    if "veg" in msg_low and "non" not in msg_low:
        remember("diet_pref", "veg")
    elif "non-veg" in msg_low or "non veg" in msg_low:
        remember("diet_pref", "non-veg")
    elif "vegan" in msg_low:
        remember("diet_pref", "vegan")

    # ---- Ask missing ----
    if not user_profile["goal"]:
        return {"reply": "What is your goal — **lose**, **gain**, or **maintain** weight?"}

    if not user_profile["diet_pref"]:
        return {"reply": "Great! Veg, non-veg or vegan?"}

    if not user_profile["age"] or not user_profile["height"] or not user_profile["weight"]:
        return {"reply": "Please share your **age**, **height (cm)**, and **weight (kg)**."}

    # ---- ALL DONE → Trigger diet service ----
    return {
        "trigger": "diet_plan",
        "reply": "Perfect! Generating your custom diet plan... 🍏",
        "goal": user_profile["goal"],
        "diet_pref": user_profile["diet_pref"],
        "age": user_profile["age"],
        "height": user_profile["height"],
        "weight": user_profile["weight"],
        "gender": user_profile["gender"] or "female"
    }


# ============================================================
#                       GYM FLOW
# ============================================================
def handle_gym_flow(msg_low):

    # detect city
    cities = ["bangalore", "chennai", "delhi", "hyderabad", "mumbai"]
    for c in cities:
        if c in msg_low:
            remember("city", c)

    # detect timing
    if "morning" in msg_low:
        remember("gym_timing", "morning")
    if "evening" in msg_low:
        remember("gym_timing", "evening")

    # detect budget
    m = re.search(r"under\s*(\d+)", msg_low)
    if m:
        remember("budget", int(m.group(1)))

    # ask missing
    if not user_profile["city"]:
        return {"reply": "Which **city** are you in? (Bangalore, Chennai, Delhi, Hyderabad, Mumbai)"}

    if not user_profile["gym_timing"]:
        return {"reply": "Do you prefer **morning** or **evening** workouts?"}

    if not user_profile["budget"]:
        return {"reply": "What is your **budget**? (Example: under 2000)"}

    # call backend
    return {
        "trigger": "gym_search",
        "reply": f"Great! Searching gyms in {user_profile['city'].title()}...",
        "city": user_profile["city"],
        "timing": user_profile["gym_timing"],
        "budget": user_profile["budget"],
    }


# ============================================================
#                   WORKOUT FLOW
# ============================================================
def handle_workout_flow(msg_low):

    if "beginner" in msg_low:
        return {"reply": "For beginners: Push-ups, squats, planks, lunges — 3 sets each."}

    if "advanced" in msg_low:
        return {"reply": "For advanced level: HIIT, weighted squats, burpees, pull-ups."}

    if "full body" in msg_low:
        return {"reply": "Full-body routine: Squats, push-ups, deadlifts, rows, planks."}

    return {"reply": "Tell me your level (beginner/advanced) or what body part you want to train!"}
