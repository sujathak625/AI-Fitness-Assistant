import streamlit as st
from ai_dashboard.services.diet_api import get_diet_plan
from ai_dashboard.config import DIET_SERVICE_URL

st.set_page_config(layout="wide")

# ---------- GLOBAL CSS FIX ----------
st.markdown("""
<style>
body, .stApp {
    background-color: #111 !important;
    color: #f5f5f5 !important;
}
h1, h2, h3, h4, h5, h6 {
    color: #ffffff !important;
}
.stExpander {
    background-color: #222 !important;
    color: #f5f5f5 !important;
}
.block-container {
    color: #f5f5f5 !important;
}
.weekly-box {
    background: #1c1c1c;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #333;
    margin-bottom: 12px;
}
.grocery-item {
    background: #1e1e1e;
    padding: 8px 12px;
    border-radius: 8px;
    margin-bottom: 5px;
    color: #fff;
}
</style>
""", unsafe_allow_html=True)

# ---------- PAGE ----------
st.title("🥗 AI Diet Planner")
st.write("Get a personalized meal plan based on your body metrics and fitness goal.")

# ---------- USER INPUT ----------
col1, col2, col3 = st.columns(3)

with col1:
    age = st.number_input("Age", min_value=10, max_value=90)
    height = st.number_input("Height (cm)", min_value=100, max_value=220)

with col2:
    weight = st.number_input("Weight (kg)", min_value=30, max_value=200)
    gender = st.selectbox("Gender", ["male", "female"])

with col3:
    goal = st.selectbox("Goal", ["lose", "gain", "maintain"])
    diet_pref = st.selectbox("Diet Preference", ["veg", "non-veg", "vegan"])

st.markdown("---")

# ---------- MAIN ACTION ----------
if st.button("✨ Generate Diet Plan"):

    st.info("Contacting diet service...")

    data = {
        "age": age,
        "gender": gender,
        "height_cm": height,
        "weight_kg": weight,
        "goal": goal,
        "dietary_pref": diet_pref
    }

    result = get_diet_plan(data)

    if "error" in result:
        st.error("❌ Diet service returned an error.")
        st.stop()

    # ---------- SUMMARY ----------
    st.subheader("📌 Your Personalized Diet Plan")

    c1, c2 = st.columns(2)
    with c1:
        st.metric("BMI", result["bmi"])
    with c2:
        st.metric("Daily Calories", result["daily_calorie_target"])

    st.success(f"**BMI Category:** {result['bmi_category']}")

    # ---------- MEAL PLAN ----------
    st.markdown("### 🍽️ Meal Plan")
    meal_emoji = {
        "breakfast": "🍳",
        "lunch": "🥗",
        "dinner": "🍲",
        "snacks": "🍎"
    }

    for meal, desc in result["meal_plan"].items():
        st.markdown(
            f"""
            <div class="weekly-box">
                <h4>{meal_emoji.get(meal, '🍽️')} {meal.capitalize()}</h4>
                <p>{desc}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ---------- WEEKLY PLAN ----------
    st.markdown("### 📅 Weekly Meal Plan")

    for day, meals in result["weekly_plan"].items():
        st.markdown(
            f"""
            <div class="weekly-box">
                <h4>📌 {day.capitalize()}</h4>
                <p><b>Breakfast:</b> {meals['breakfast']}</p>
                <p><b>Lunch:</b> {meals['lunch']}</p>
                <p><b>Dinner:</b> {meals['dinner']}</p>
                <p><b>Snacks:</b> {meals['snacks']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ---------- GROCERY LIST (NOW SAFE) ----------
    st.markdown("### 🛒 Grocery List")

    grocery = result.get("grocery_list", [])

    def get_emoji_for_item(item: str) -> str:
        it = item.lower()
        mapping = {
            "leaf": "🥬", "spinach": "🥬", "lettuce": "🥬", "kale": "🥬",
            "tomato": "🍅",
            "carrot": "🥕",
            "cheese": "🧀", "paneer": "🧀",
            "milk": "🥛", "yogurt": "🥛",
            "apple": "🍎", "banana": "🍌",
            "rice": "🍚", "bread": "🍞", "oats": "🥣",
            "chicken": "🍗", "fish": "🐟", "egg": "🥚",
            "nuts": "🥜", "peanut": "🥜",
            "protein": "💪",
            "dal": "🥣", "lentil": "🥣",
            "salad": "🥗", "veggies": "🥦",
        }
        for k, e in mapping.items():
            if k in it:
                return e
        return "🛒"

    if grocery:
        for item in grocery:
            emoji = get_emoji_for_item(item)
            display_item = item.strip().capitalize()
            st.markdown(
                f"""
                <div class="grocery-item">
                    {emoji} {display_item}
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.warning("No grocery items found.")
