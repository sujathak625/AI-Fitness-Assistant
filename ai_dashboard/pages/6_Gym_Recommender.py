import streamlit as st
import requests
from ai_dashboard.config import GYM_SERVICE_URL

st.title("🏋️‍♂️ AI Gym Recommender & Planner")
st.write("Find the best gyms near you and get a personalized weekly workout plan.")

# -----------------------------
# City Input (fixed list for assignment)
# -----------------------------
cities = ["Bangalore", "Chennai", "Hyderabad", "Mumbai"]
city_input = st.selectbox("Select Your City", cities)

# -----------------------------
# Goal Input
# -----------------------------
goal = st.selectbox(
    "Your Fitness Goal",
    ["general_fitness", "fat_loss", "muscle_gain", "flexibility"]
)

# -----------------------------
# Fitness Level
# -----------------------------
level = st.selectbox("Your fitness level", ["beginner", "intermediate", "advanced"])

# -----------------------------
# Days Per Week
# -----------------------------
days = st.slider("How many days will you train per week?", 1, 7, 4)

# -----------------------------
# Radius Filter
# -----------------------------
radius = st.slider("Search Radius (km) — set 0 to ignore distance filter", 0, 30, 5)

# -----------------------------
# Budget Filter
# -----------------------------
budget = st.selectbox("Budget Range (Optional)", ["None", "low", "mid", "high"])

# -----------------------------
# Morning Classes Filter
# -----------------------------
morning_only = st.checkbox("Show only gyms with morning classes")

# -----------------------------
# Safety: initialize variables so they exist outside the button block
# -----------------------------
gyms = []
plan = {}

# -----------------------------
# City coords (assignment fixed)
# -----------------------------
city_coords = {
    "Bangalore": (12.9716, 77.5946),
    "Chennai": (13.0827, 80.2707),
    "Hyderabad": (17.3850, 78.4867),
    "Mumbai": (19.0760, 72.8777)
}

# -----------------------------
# Helper to call backend safely
# -----------------------------
def fetch_gyms(params):
    try:
        res = requests.get(f"{GYM_SERVICE_URL}/gyms", params=params, timeout=6)
        if res.status_code == 200:
            return res.json()
        else:
            st.error(f"Gym service error: {res.status_code}")
            return []
    except Exception as e:
        st.error(f"Error fetching gyms: {e}")
        return []

def fetch_plan(payload):
    try:
        res = requests.post(f"{GYM_SERVICE_URL}/plan", json=payload, timeout=6)
        if res.status_code == 200:
            return res.json()
        else:
            st.error(f"Plan service error: {res.status_code}")
            return {}
    except Exception as e:
        st.error(f"Error fetching plan: {e}")
        return {}

# -----------------------------
# On Submit
# -----------------------------
if st.button("🔎 Get Recommendations"):
    st.info("Fetching recommendations...")

    # normalize city and coordinates
    city_clean = city_input.strip()
    lat, lon = city_coords.get(city_clean, (None, None))

    if lat is None:
        st.error("City not supported.")
    else:
        # prepare params for gym API
        params = {
            "lat": lat,
            "lon": lon,
            "city": city_clean,
            "goal": goal,
            "radius_km": radius,
            "morning_only": morning_only
        }
        if budget != "None":
            params["budget"] = budget

        gyms = fetch_gyms(params)

        # plan payload
        plan_payload = {
            "goal": goal,
            "level": level,
            "days_per_week": days
        }
        plan = fetch_plan(plan_payload)

        st.success(f"📍 Showing results for **{city_clean}** within **{radius} km**")
        st.write("---")

        # 1) Gyms: styled cards with explicit colors to avoid theme issues
        st.header("🏋️ Nearby Gym Recommendations")
        if not gyms:
            st.warning("No gyms found nearby. Try increasing radius or changing filters.")
        else:
            for g in gyms:
                # guard missing keys
                g_name = g.get("name", "Unknown")
                g_city = g.get("city", city_clean)
                g_rating = g.get("rating", "N/A")
                g_distance = g.get("distance_km", "N/A")
                g_price_tier = g.get("price_tier", "N/A")
                g_membership = g.get("membership_price", "N/A")
                g_amenities = ", ".join(g.get("amenities", []))
                g_opening = g.get("opening_hours", "N/A")
                g_morning = "Yes" if g.get("morning_classes", False) else "No"

                st.markdown(
                    f"""
                    <div style="
                        background-color:#f0f0f0;
                        padding:14px;
                        border-radius:10px;
                        margin-bottom:12px;
                        color:#000000;
                        border:1px solid #d0d0d0;">
                        <h4 style="margin:0 0 6px 0;color:#000;">🏋️ {g_name}</h4>
                        <p style="margin:2px 0;color:#000;">
                            ⭐ <b>{g_rating}</b> &nbsp; | &nbsp; 📏 {g_distance} km away
                        </p>
                        <p style="margin:2px 0;color:#000;"><b>City:</b> {g_city}</p>
                        <p style="margin:2px 0;color:#000;"><b>Price Tier:</b> {g_price_tier} &nbsp; | &nbsp; ₹{g_membership}</p>
                        <p style="margin:2px 0;color:#000;"><b>Amenities:</b> {g_amenities}</p>
                        <p style="margin:2px 0;color:#000;"><b>Opening Hours:</b> {g_opening} &nbsp; | &nbsp; <b>Morning Classes:</b> {g_morning}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.write("---")

        # 2) Weekly plan (styled)
        st.header("📅 Weekly Workout Plan")
        weekly_plan = plan.get("weekly_plan", {})

        if not weekly_plan:
            st.warning("No plan generated.")
        else:
            for day, tasks in weekly_plan.items():
                st.markdown(
                    f"""
                    <div style="
                        background-color:#f0f0f0;
                        border-radius:8px;
                        padding:12px;
                        margin-bottom:10px;
                        border:1px solid #d0d0d0;
                        color:#000;">
                        <h4 style="margin:0 0 6px 0;color:#000;">📌 {day.replace('_', ' ').title()}</h4>
                        <ul style="margin:6px 0 0 18px;">
                            {''.join([f"<li style='color:#000;margin:2px 0;'>{t}</li>" for t in tasks])}
                        </ul>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.write("---")

        # 3) Suggested challenges (static)
        st.header("🔥 Suggested Fitness Challenges")
        challenge_map = {
            "fat_loss": [
                "🔥 10k Steps Challenge",
                "⏱ Daily 20-Min HIIT Challenge",
                "🥗 7-Day Clean Eating Plan"
            ],
            "muscle_gain": [
                "🏋️ 5×5 Strength Challenge",
                "💪 Progressive Overload 14-Day Program",
                "🍗 High-Protein Diet Week"
            ],
            "flexibility": [
                "🧘 15-Day Yoga Flex Program",
                "🤸 Daily Mobility Routine",
                "🦵 Hamstring Stretch Challenge"
            ],
            "general_fitness": [
                "🚶 Walk 5km Daily",
                "🏃 Cardio Mix 30-Day Challenge",
                "💪 Core Strength Week"
            ]
        }
        for c in challenge_map.get(goal, []):
            st.markdown(f"- {c}")

        st.success("🎉 Your personalized gym & workout recommendations are ready!")


else:
    st.info("Select options above and click '🔎 Get Recommendations' to fetch gyms and a weekly plan.")
