from datetime import datetime
from app.utils.storage import load_data, save_data

def calculate_streak(history):
    streak = 0
    history_sorted = sorted(history, key=lambda x: x["date"], reverse=True)
    last_date = None

    for entry in history_sorted:
        date = datetime.fromisoformat(entry["date"]).date()

        if last_date is None:
            last_date = date

        if last_date == date and entry["worked_out"]:
            streak += 1

        elif (last_date - date).days == 1 and entry["worked_out"]:
            streak += 1

        else:
            break

        last_date = date

    return streak


def predict_skip_probability(history):
    if len(history) < 3:
        return 0.3

    last_week = history[-7:]
    skips = sum(1 for h in last_week if not h["worked_out"])
    streak = calculate_streak(history)

    if skips >= 3:
        return 0.85
    if streak >= 3:
        return 0.25
    if streak == 0:
        return 0.60

    return 0.50


def motivational_message(prob):
    if prob > 0.8:
        return "⚠ You’ve missed several days. Try just 5 minutes today ❤️"
    if prob > 0.6:
        return "Let's get back on track. Even a small workout helps 💪"
    if prob > 0.4:
        return "You're doing okay — stay consistent ✨"
    return "🔥 Amazing streak! Keep going!"


def log_workout(user_id, worked_out):
    db = load_data()

    if user_id not in db:
        db[user_id] = []

    db[user_id].append({
        "date": datetime.now().isoformat(),
        "worked_out": worked_out
    })

    save_data(db)
    return True


def generate_report(user_id):
    db = load_data()
    history = db.get(user_id, [])

    if not history:
        return {
            "user_id": user_id,
            "streak": 0,
            "skip_probability": 0.5,
            "message": "Start your fitness journey today! 💪",
            "history": []
        }

    streak = calculate_streak(history)
    prob = predict_skip_probability(history)
    msg = motivational_message(prob)

    return {
        "user_id": user_id,
        "streak": streak,
        "skip_probability": round(prob, 2),
        "message": msg,
        "history": history
    }
