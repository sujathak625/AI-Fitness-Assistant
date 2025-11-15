from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import math

app = FastAPI(title="AI Diet Planner Service")


# -----------------------
# Data Models
# -----------------------

class DietInput(BaseModel):
    age: int
    gender: str
    height_cm: float
    weight_kg: float
    goal: str              # lose / gain / maintain
    dietary_pref: Optional[str] = None   # veg / non-veg / vegan


class DietPlan(BaseModel):
    bmi: float
    bmi_category: str
    daily_calorie_target: int
    meal_plan: dict
    weekly_plan: dict
    grocery_list: list


# -----------------------
# Helper Functions
# -----------------------

def calculate_bmi(weight, height):
    h = height / 100
    return round(weight / (h * h), 2)


def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    if 18.5 <= bmi <= 24.9:
        return "Normal weight"
    if 25 <= bmi <= 29.9:
        return "Overweight"
    return "Obese"


def calculate_calories(gender, weight, height, age, goal):
    # Mifflin St. Jeor Equation
    if gender.lower() == "male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    tdee = bmr * 1.375  # lightly active

    if goal == "lose":
        tdee -= 400
    elif goal == "gain":
        tdee += 400

    return int(tdee)


# -----------------------
# Meal Plan Templates
# -----------------------

def get_meal_plan(goal, pref):
    goal = goal.lower()
    pref = (pref or "non-veg").lower()

    # ---- VEG --------
    if pref == "veg":
        if goal == "lose":
            return {
                "breakfast": "Oats + chia + fruit",
                "lunch": "Veg salad + dal",
                "dinner": "Grilled paneer + veggies",
                "snacks": "Green tea + nuts"
            }
        if goal == "gain":
            return {
                "breakfast": "Peanut butter toast + banana",
                "lunch": "Rice + dal + paneer",
                "dinner": "Pulao + curd",
                "snacks": "Protein shake"
            }

    # ---- NON VEG ------
    if goal == "lose":
        return {
            "breakfast": "Egg whites + fruit",
            "lunch": "Chicken salad",
            "dinner": "Grilled fish + veggies",
            "snacks": "Greek yogurt"
        }

    if goal == "gain":
        return {
            "breakfast": "Eggs + toast + peanut butter",
            "lunch": "Rice + chicken curry",
            "dinner": "Pasta + chicken",
            "snacks": "Protein shake"
        }

    # ---- MAINTAIN ----
    return {
        "breakfast": "Oats / eggs",
        "lunch": "Balanced plate (carbs + protein + veggies)",
        "dinner": "Light protein + veggies",
        "snacks": "Nuts / yogurt"
    }


def create_weekly_plan(meal_plan):
    return {
        "monday": meal_plan,
        "tuesday": meal_plan,
        "wednesday": meal_plan,
        "thursday": meal_plan,
        "friday": meal_plan,
        "saturday": meal_plan,
        "sunday": meal_plan
    }


def extract_grocery(meals: dict):
    words = []
    for meal in meals.values():
        cleaned = meal.replace("+", " ").replace(",", " ")
        words.extend(cleaned.split())
    return sorted(list(set(words)))


# -----------------------
# Endpoints
# -----------------------

@app.get("/health")
async def health():
    return {"status": "ok", "service": "diet-service"}


@app.post("/diet/plan", response_model=DietPlan)
async def diet_plan(data: DietInput):

    bmi = calculate_bmi(data.weight_kg, data.height_cm)
    category = get_bmi_category(bmi)
    calories = calculate_calories(data.gender, data.weight_kg, data.height_cm, data.age, data.goal)

    meal_plan = get_meal_plan(data.goal, data.dietary_pref)
    weekly = create_weekly_plan(meal_plan)
    grocery = extract_grocery(meal_plan)

    return DietPlan(
        bmi=bmi,
        bmi_category=category,
        daily_calorie_target=calories,
        meal_plan=meal_plan,
        weekly_plan=weekly,
        grocery_list=grocery
    )
