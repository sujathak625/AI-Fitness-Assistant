# ai-services/chat-service/app/workout_engine.py

from utils import contains_any


# -------------------------------------------
# 1. Fat Loss Workout Generator
# -------------------------------------------
def fat_loss_workout(level="beginner"):
    if level == "beginner":
        return (
            "🔥 **Beginner Fat-Loss Workout (15 min)**\n"
            "• 20 jumping jacks\n"
            "• 15 bodyweight squats\n"
            "• 10 knee pushups\n"
            "• 20 mountain climbers\n"
            "• 30 sec plank\n"
            "Repeat 2 times\n"
        )
    if level == "intermediate":
        return (
            "🔥 **Intermediate Fat-Loss Workout (20 min)**\n"
            "• 30 jumping jacks\n"
            "• 20 squats\n"
            "• 12 pushups\n"
            "• 30 mountain climbers\n"
            "• 45 sec plank\n"
            "Repeat 3 times\n"
        )
    # advanced
    return (
        "🔥 **Advanced Fat-Loss Workout (25 min)**\n"
        "• 40 jumping jacks\n"
        "• 20 squat jumps\n"
        "• 15 pushups\n"
        "• 1 min mountain climbers\n"
        "• 1 min plank\n"
        "Repeat 3 times\n"
    )


# -------------------------------------------
# 2. Strength / Muscle Gain Workout
# -------------------------------------------
def strength_workout(level="beginner"):
    if level == "beginner":
        return (
            "💪 **Beginner Strength Workout (20 min)**\n"
            "• 12 pushups\n"
            "• 10 lunges (each leg)\n"
            "• 15 squats\n"
            "• 10 dips\n"
            "Repeat 3 times\n"
        )
    if level == "intermediate":
        return (
            "💪 **Intermediate Strength Workout (25 min)**\n"
            "• 20 pushups\n"
            "• 15 lunges (each leg)\n"
            "• 20 squats\n"
            "• 15 dips\n"
            "Repeat 3 times\n"
        )
    return (
        "💪 **Advanced Strength Workout (30 min)**\n"
        "• 25 pushups\n"
        "• 20 lunges each leg\n"
        "• 25 squats\n"
        "• 20 dips\n"
        "Repeat 4 times\n"
    )


# -------------------------------------------
# 3. Quick 10-minute warmup
# -------------------------------------------
def warmup_10min():
    return (
        "⏱️ **Quick 10-Min Warmup**\n"
        "• 1 min marching\n"
        "• 1 min arm circles\n"
        "• 1 min hip rotation\n"
        "• 2 min spot jogging\n"
        "• 1 min jumping jacks\n"
        "• 2 min stretching\n"
    )


# -------------------------------------------
# 4. Flexibility / Yoga Routine
# -------------------------------------------
def flexibility_routine():
    return (
        "🧘 **Flexibility / Yoga Routine (10 min)**\n"
        "• Cat-cow stretch – 1 min\n"
        "• Child's pose – 1 min\n"
        "• Forward fold – 1 min\n"
        "• Hip opener stretch – 2 min\n"
        "• Downward dog – 2 min\n"
        "• Spine twist – 2 min\n"
    )


# -------------------------------------------
# 5. Cardio / HIIT
# -------------------------------------------
def hiit_routine():
    return (
        "🏃 **HIIT Fat-Burner (12 min)**\n"
        "• 30 sec high knees\n"
        "• 30 sec rest\n"
        "• 30 sec burpees\n"
        "• 30 sec rest\n"
        "• 30 sec mountain climbers\n"
        "• 30 sec rest\n"
        "Repeat 3 rounds\n"
    )


# -------------------------------------------
# 6. Main Workout Engine
# -------------------------------------------
def generate_workout_response(message: str, goal="fat_loss", level="beginner"):
    msg = message.lower()

    # Quick warmup
    if contains_any(msg, ["warmup", "warm up", "warm-up"]):
        return warmup_10min()

    # Flexibility
    if contains_any(msg, ["stretch", "flexibility", "yoga"]):
        return flexibility_routine()

    # HIIT
    if contains_any(msg, ["hiit", "cardio", "fat burn"]):
        return hiit_routine()

    # Strength / muscle gain
    if contains_any(msg, ["strength", "muscle", "build"]):
        return strength_workout(level)

    # Fat loss (default)
    return fat_loss_workout(level)
