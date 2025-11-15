from ..app.main import calculate_angle, evaluate_angle, extract_landmarks


def test_calculate_angle_90_deg():
    a = [0, 1]
    b = [0, 0]
    c = [1, 0]
    angle = calculate_angle(a, b, c)
    assert round(angle) == 90

def test_calculate_angle_straight_line():
    a = [0, 0]
    b = [1, 1]
    c = [2, 2]
    angle = calculate_angle(a, b, c)
    assert round(angle) == 0

def test_evaluate_angle_squat_good():
    feedback, score = evaluate_angle("squat", 120)
    assert feedback == "Good squat depth"
    assert score == 1.0

def test_evaluate_angle_pushup_low():
    feedback, score = evaluate_angle("pushup", 80)
    assert feedback == "Too low – risk of shoulder strain"
    assert score == 0.6

def test_extract_landmarks_squat():
    class FakeLM:
        def __init__(self):
            self.x = 0.5
            self.y = 0.5
    lm = [FakeLM() for _ in range(33)]
    a, b, c = extract_landmarks(lm, "squat")
    assert a is not None and b is not None and c is not None
