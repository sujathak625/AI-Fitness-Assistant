# ai-services/chat-service/app/diet_engine.py

from utils import contains_any


# -------------------------------------
# 1. Calorie & Macro Calculation
# -------------------------------------
def calculate_macros(weight_kg: float, goal: str = "fat_loss"):
    """
    Return recommended protein, carbs, fats based on fitness goal.
    """

    if goal == "muscle_gain":
        protein = round(weight_kg * 1.8)
        carbs = round(weight_kg * 4)
        fats = round(weight_kg * 1.0)

    elif goal == "maintenance":
        protein = round(weight_kg * 1.2)
        carbs = round(weight_kg * 3)
        fats = round(weight_kg * 0.8)

    else:  # fat loss
        protein = round(weight_kg * 1.5)
        carbs = round(weight_kg * 2)
        fats = round(weight_kg * 0.7)

    return {
        "protein_g": protein,
        "carbs_g": carbs,
        "fats_g": fats
    }


# -------------------------------------
# 2. Vegetarian Diet Plan
# -------------------------------------
def vegetarian_plan(goal="fat_loss"):
    if goal == "muscle_gain":
        return (
            "🌱 **Vegetarian Muscle-Gain Diet**\n"
            "• Breakfast: Oats + whey/pea protein\n"
            "• Lunch: Paneer + rice + veggies\n"
            "• Dinner: Soya chunks + dal + roti\n"
            "• Snacks: Nuts, yogurt, peanut butter\n"
        )

    if goal == "maintenance":
        return (
            "🌱 **Vegetarian Balanced Diet**\n"
            "• Breakfast: Poha/upma + nuts\n"
            "• Lunch: Dal + rice + veggies\n"
            "• Dinner: Paneer subji + roti\n"
            "• Snacks: Fruits, seeds\n"
        )

    return (
        "🌱 **Vegetarian Fat-Loss Diet**\n"
        "• Breakfast: Oats + chia seeds\n"
        "• Lunch: Dal + salad + 1 roti\n"
        "• Dinner: Paneer + steamed veggies\n"
        "• Snacks: fruits, green tea\n"
    )


# -------------------------------------
# 3. Non-Vegetarian Diet Plan
# -------------------------------------
def nonveg_plan(goal="fat_loss"):
    if goal == "muscle_gain":
        return (
            "🍗 **Muscle-Gain Diet**\n"
            "• Breakfast: Eggs + oats\n"
            "• Lunch: Chicken + rice + veggies\n"
            "• Dinner: Fish + salad\n"
            "• Snacks: Nuts, yogurt, whey protein\n"
        )

    if goal == "maintenance":
        return (
            "🍗 **Balanced Diet**\n"
            "• Breakfast: Eggs + toast\n"
            "• Lunch: Chicken + roti + veggies\n"
            "• Dinner: Light soup + grilled fish\n"
            "• Snacks: Fruits, seeds\n"
        )

    return (
        "🔥 **Fat-Loss Diet**\n"
        "• Breakfast: Eggs/omelette\n"
        "• Lunch: Grilled chicken + veggies\n"
        "• Dinner: Soup + salad\n"
        "• Snacks: green tea, almonds\n"
    )


# -------------------------------------
# 4. Hunger Response
# -------------------------------------
def hunger_suggestion():
    return (
        "🍏 You seem hungry! Here are healthy snack options:\n"
        "• Greek yogurt\n"
        "• Nuts & seeds\n"
        "• A fruit (apple, banana)\n"
        "• Paneer cubes\n"
        "• Boiled eggs\n"
        "Eating every 3–4 hours helps stabilize energy. 💪"
    )


# -------------------------------------
# 5. Time-of-Day Based Suggestions
# -------------------------------------
def meal_suggestion(time_keyword):
    if "breakfast" in time_keyword:
        return (
            "🌅 **Breakfast ideas:**\n"
            "• Oats + fruits\n"
            "• Eggs + toast\n"
            "• Poha/upma + nuts\n"
        )

    if "lunch" in time_keyword:
        return (
            "🍱 **Lunch ideas:**\n"
            "• Paneer/chicken bowl\n"
            "• Dal + rice + veggies\n"
            "• Roti + sabji + salad\n"
        )

    if "dinner" in time_keyword:
        return (
            "🌙 **Dinner ideas:**\n"
            "• Soup + salad\n"
            "• Paneer/chicken + veggies\n"
            "• Light stir-fry meal\n"
        )

    return None


# -------------------------------------
# 6. Main Diet Engine
# -------------------------------------
def generate_diet_response(message: str, goal: str = "fat_loss", weight_kg: float = 70):
    msg = message.lower()

    # Hunger
    if "hungry" in msg:
        return hunger_suggestion()

    # Breakfast/lunch/dinner suggestions
    for t in ["breakfast", "lunch", "dinner"]:
        if t in msg:
            return meal_suggestion(t)

    # Vegetarian
    if contains_any(msg, ["veg", "vegetarian", "vegan", "plant based"]):
        return vegetarian_plan(goal)

    # Non-veg (default)
    return nonveg_plan(goal)
