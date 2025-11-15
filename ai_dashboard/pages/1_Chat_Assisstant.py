import streamlit as st
import requests
from ai_dashboard.config import CHAT_SERVICE_URL, DIET_SERVICE_URL, GYM_SERVICE_URL

st.set_page_config(page_title="AI Gym Chat Assistant", layout="wide")

st.title("💬 AI Gym Assistant Chatbot")
st.caption("Diet • Workouts • Gyms • Motivation")

# -----------------------------------------
# Session State
# -----------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

def ask_chat(msg):
    try:
        r = requests.post(f"{CHAT_SERVICE_URL}/chat/respond", json={"msg": msg}, timeout=10)
        return r.json()
    except:
        return {"reply": "❌ Server not reachable. Please try again."}

def call_diet(payload):
    try:
        r = requests.post(f"{DIET_SERVICE_URL}/diet/plan", json=payload, timeout=10)
        return r.json()
    except:
        return {"error": "diet service error"}

def call_gym(city, timing, budget):
    try:
        r = requests.get(f"{GYM_SERVICE_URL}/gyms/search?city={city}&timing={timing}&budget={budget}")
        return r.json()
    except:
        return {"error": "gym service error"}

# -----------------------------------------
# Render bubbles
# -----------------------------------------
def user_bubble(msg):
    st.markdown(f"""
    <div style='text-align:right; margin:10px'>
        <div style='display:inline-block; padding:10px; background:#4A90E2; color:white; border-radius:10px'>
            {msg}
        </div>
    </div>
    """, unsafe_allow_html=True)

def bot_bubble(msg):
    st.markdown(f"""
    <div style='text-align:left; margin:10px'>
        <div style='display:inline-block; padding:10px; background:#333; color:white; border-radius:10px'>
            {msg}
        </div>
    </div>
    """, unsafe_allow_html=True)

# show history
for m in st.session_state.messages:
    (user_bubble if m["role"]=="user" else bot_bubble)(m["text"])

# -----------------------------------------
# Input
# -----------------------------------------
msg = st.chat_input("Type your message...")

if msg:
    user_bubble(msg)
    st.session_state.messages.append({"role": "user", "text": msg})

    res = ask_chat(msg)

    # ---------- DIET TRIGGER ----------
    if res.get("trigger") == "diet_plan":
        diet = call_diet({
            "age": res["age"],
            "gender": res["gender"],
            "height_cm": res["height"],
            "weight_kg": res["weight"],
            "goal": res["goal"],
            "dietary_pref": res["diet_pref"]
        })

        if "error" in diet:
            reply = "❌ Failed to fetch diet plan."
        else:
            reply = f"""
            **🍽️ Your Personalized Diet Plan**

            **BMI:** {diet['bmi']}  
            **Calories/day:** {diet['daily_calorie_target']}  
            **Category:** {diet['bmi_category']}

            🥗 **Breakfast:** {diet['meal_plan']['breakfast']}  
            🍛 **Lunch:** {diet['meal_plan']['lunch']}  
            🍲 **Dinner:** {diet['meal_plan']['dinner']}  
            🍎 **Snacks:** {diet['meal_plan']['snacks']}
            """

        bot_bubble(reply)
        st.session_state.messages.append({"role":"assistant", "text":reply})

    # ---------- GYM TRIGGER ----------
    elif res.get("trigger") == "gym_search":
        gyms = call_gym(res["city"], res["timing"], res["budget"])
        if "error" in gyms:
            reply = "❌ Gym service unavailable."
        else:
            gym_list = "\n".join([f"🏋️ {g['name']} — ₹{g['price']}/month" for g in gyms])
            reply = f"Here are the gyms I found:\n\n{gym_list}"

        bot_bubble(reply)
        st.session_state.messages.append({"role":"assistant", "text":reply})

    # ---------- NORMAL BOT RESPONSE ----------
    else:
        bot_bubble(res.get("reply", "🤖 No response"))
        st.session_state.messages.append({"role":"assistant", "text":res.get("reply","")})
