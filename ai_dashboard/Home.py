import streamlit as st

st.set_page_config(
    page_title="AI Gym & Fitness Assistant",
    page_icon="💪",
)

# -----------------------------------
# MAIN HOMEPAGE CONTENT
# -----------------------------------
st.title("🤖 AI Gym & Fitness Assistant")
st.subheader("Your all-in-one AI-powered fitness ecosystem")

st.markdown("""
Welcome to the **AI Gym & Fitness Assistant** — a unified fitness platform powered by AI, 
IoT, and intelligent automation.  
This system integrates multiple microservices to help you track, plan, and 
improve your fitness journey.

---

## 💡 What this App Offers

### 🏋️ 1. AI Workout Detector  
Upload workout images and get:
- Exercise identification  
- Angle analysis  
- Posture corrections  
- Performance score  

---

### 🥗 2. AI Diet Planner  
Based on your **BMI, goal, gender, food preference**, it provides:  
- Personalized daily meal plan  
- Weekly meal plan  
- Automatically generated grocery list  

---

### 💬 3. Virtual Gym Buddy (AI Chatbot)  
Smart conversational coach that can:
- Understand your message  
- Recommend workouts & diet  
- Track habits  
- Give motivational support  
- Adapt personality and fitness goals  

---

### 📊 4. Habit Tracker  
Log daily habits with:
- Interactive table  
- Summary metrics  
- Clean timestamp support  
- History view + optional reset  

---

### 🧪 5. IoT Smart Gym Integration  
Simulated IoT service offering:
- Realtime sensor signals  
- Equipment status  
- Smart recommendations  

---

### 🏋️‍♂️ 6. Gym Recommender & Planner  
Find gyms based on:
- Your city  
- Budget  
- Morning/evening preference  
- Fitness goal  
- Distance  

Also provides:
- 7-day weekly workout plan  
- Fitness challenge suggestions  

---


""")
