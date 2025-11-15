from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel
from typing import List
import numpy as np
import cv2
import mediapipe as mp
import math

app = FastAPI(title="AI Gym Trainer Service (Multi-Exercise)")

mp_pose = mp.solutions.pose


# --------------------- MODELS ---------------------
class PoseResult(BaseModel):
    file_name: str
    exercise: str
    pose_detected: bool
    angle: float | None
    feedback: str
    performance_score: float


# --------------------- UTILITIES ------------------
def calculate_angle(a, b, c):
    """Return the angle (in degrees) between three points a-b-c."""
    a, b, c = np.array(a), np.array(b), np.array(c)
    radians = math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0])
    angle = abs(radians * 180.0 / math.pi)
    return 360 - angle if angle > 180.0 else angle


def evaluate_angle(exercise, angle):
    """Return feedback and score based on exercise type and angle thresholds."""
    exercise = exercise.lower()

    if exercise == "squat":
        if angle > 160:
            return "Standing too tall", 0.4
        elif 90 <= angle <= 160:
            return "Good squat depth", 1.0
        elif angle < 90:
            return "Too low – control your depth", 0.6

    elif exercise == "pushup":
        if angle > 160:
            return "Arms too straight, lower your body", 0.4
        elif 90 <= angle <= 160:
            return "Good push-up depth", 1.0
        elif angle < 90:
            return "Too low – risk of shoulder strain", 0.6

    elif exercise == "plank":
        if 170 <= angle <= 180:
            return "Perfect plank posture", 1.0
        elif angle < 170:
            return "Hips too low", 0.5
        else:
            return "Hips too high", 0.6

    elif exercise == "lunge":
        if angle > 160:
            return "Incomplete lunge – go lower", 0.5
        elif 90 <= angle <= 160:
            return "Good lunge form", 1.0
        elif angle < 90:
            return "Too deep – unsafe range", 0.6

    elif exercise == "bicep_curl":
        if angle > 150:
            return "Arm extended – ready position", 0.5
        elif 45 <= angle <= 150:
            return "Good curl range", 1.0
        elif angle < 45:
            return "Curl too tight", 0.7

    return "Unrecognized exercise", 0.0


def extract_landmarks(lm, exercise):
    """Select landmarks depending on exercise type."""
    if exercise in ["squat", "lunge"]:
        a = [lm[mp_pose.PoseLandmark.LEFT_HIP.value].x, lm[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        b = [lm[mp_pose.PoseLandmark.LEFT_KNEE.value].x, lm[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
        c = [lm[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, lm[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
    elif exercise in ["pushup", "bicep_curl"]:
        a = [lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        b = [lm[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, lm[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        c = [lm[mp_pose.PoseLandmark.LEFT_WRIST.value].x, lm[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
    elif exercise == "plank":
        a = [lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, lm[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        b = [lm[mp_pose.PoseLandmark.LEFT_HIP.value].x, lm[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        c = [lm[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, lm[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
    else:
        a, b, c = None, None, None
    return a, b, c

def classify_exercise(landmarks):
    """
    Stronger, more accurate multi-exercise classifier.
    """
    try:
        left_hip = landmarks[23]
        right_hip = landmarks[24]
        left_knee = landmarks[25]
        right_knee = landmarks[26]
        left_ankle = landmarks[27]
        right_ankle = landmarks[28]
        left_shoulder = landmarks[11]
        right_shoulder = landmarks[12]
        left_elbow = landmarks[13]
        right_elbow = landmarks[14]
        left_wrist = landmarks[15]
        right_wrist = landmarks[16]

        # ----------------------------------------------------
        # 1️⃣ LUNGE (robust detection)
        # ----------------------------------------------------
        # Knee angles (left and right)
        left_knee_angle = calculate_angle(
            [left_hip.x, left_hip.y],
            [left_knee.x, left_knee.y],
            [left_ankle.x, left_ankle.y]
        )

        right_knee_angle = calculate_angle(
            [right_hip.x, right_hip.y],
            [right_knee.x, right_knee.y],
            [right_ankle.x, right_ankle.y]
        )

        knee_angle_diff = abs(left_knee_angle - right_knee_angle)

        # One foot forward (difference in y position)
        leg_forward = abs(left_ankle.y - right_ankle.y) > 0.10

        # Hip displacement (side shift)
        hip_forward = abs(left_hip.x - right_hip.x) > 0.08

        # Final lunge condition
        if knee_angle_diff > 18 and leg_forward and hip_forward:
            return "lunge", 0.96


        # ----------------------------------------------------
        # 2️⃣ PUSHUP
        # ----------------------------------------------------
        upper_body_horizontal = abs(left_shoulder.y - left_hip.y) < 0.15
        arm_straightness = abs(left_wrist.y - left_elbow.y) < 0.15

        if upper_body_horizontal and arm_straightness:
            return "pushup", 0.92

        # ----------------------------------------------------
        # 3️⃣ PLANK
        # ----------------------------------------------------
        if upper_body_horizontal and abs(left_shoulder.y - left_wrist.y) < 0.05:
            return "plank", 0.88

        # ----------------------------------------------------
        # 4️⃣ SQUAT
        # ----------------------------------------------------
        knee_angle = left_knee_angle
        hip_drop = left_hip.y

        if knee_angle < 120 and hip_drop > 0.47:
            return "squat", 0.95

        # ----------------------------------------------------
        # 5️⃣ JUMPING JACK
        # ----------------------------------------------------
        arms_wide = abs(left_wrist.x - right_wrist.x) > 0.80
        legs_wide = abs(left_ankle.x - right_ankle.x) > 0.50

        if arms_wide and legs_wide:
            return "jumping_jack", 0.90

        return "unknown", 0.50

    except:
        return "unknown", 0.0





# --------------------- ROUTES ---------------------
@app.get("/health")
async def health_check():
    return {"status": "ok", "supported_exercises": ["squat", "pushup", "plank", "lunge", "bicep_curl"]}

@app.post("/workouts/frame")
async def analyze_single_frame(file: UploadFile = File(...)):
    """
    Analyze a single image:
    - Auto detect exercise
    - Extract landmarks
    - Calculate angle
    - Generate feedback
    - Estimate reps
    """
    data = await file.read()
    np_arr = np.frombuffer(data, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if img is None:
        return {
            "file_name": file.filename,
            "exercise": "unknown",
            "pose_detected": False,
            "angle": None,
            "feedback": "Invalid image format",
            "performance_score": 0.0,
            "rep_count": 0
        }

    with mp_pose.Pose(static_image_mode=True) as pose:
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        res = pose.process(img_rgb)

        if not res.pose_landmarks:
            return {
                "file_name": file.filename,
                "exercise": "unknown",
                "pose_detected": False,
                "angle": None,
                "feedback": "No person detected",
                "performance_score": 0.0,
                "rep_count": 0
            }

        lm = res.pose_landmarks.landmark

        # Auto exercise detection
        exercise, confidence = classify_exercise(lm)

        # Get joints for angle calculation
        a, b, c = extract_landmarks(lm, exercise)

        if not a or not b or not c:
            return {
                "file_name": file.filename,
                "exercise": exercise,
                "pose_detected": True,
                "angle": None,
                "feedback": "Unable to compute angle",
                "performance_score": 0.0,
                "rep_count": 0
            }

        # Angle
        angle = calculate_angle(a, b, c)

        # Feedback
        feedback, score = evaluate_angle(exercise, angle)

        # Rep estimation
        rep_count = 1 if score >= 0.8 else 0

        return {
            "file_name": file.filename,
            "exercise": exercise,
            "confidence": round(confidence, 2),
            "pose_detected": True,
            "angle": round(angle, 2),
            "feedback": feedback,
            "performance_score": round(score, 2),
            "rep_count": rep_count
        }

@app.post("/workouts/batch")
async def analyze_batch_auto(files: List[UploadFile] = File(...)):
    """
    Analyze multiple images:
    - Auto detect exercise for each image
    - Calculate angles
    - Provide feedback
    - Score performance
    - Return summary statistics
    """

    results = []
    total_score = 0
    valid_count = 0
    exercise_counts = {}

    with mp_pose.Pose(static_image_mode=True) as pose:
        for file in files:
            data = await file.read()
            np_arr = np.frombuffer(data, np.uint8)
            img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            if img is None:
                results.append({
                    "file_name": file.filename,
                    "exercise": "unknown",
                    "pose_detected": False,
                    "angle": None,
                    "feedback": "Invalid image",
                    "performance_score": 0.0,
                    "rep_count": 0
                })
                continue

            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            res = pose.process(img_rgb)

            if not res.pose_landmarks:
                results.append({
                    "file_name": file.filename,
                    "exercise": "unknown",
                    "pose_detected": False,
                    "angle": None,
                    "feedback": "No person detected",
                    "performance_score": 0.0,
                    "rep_count": 0
                })
                continue

            lm = res.pose_landmarks.landmark

            # 1️⃣ Auto exercise detection
            exercise, confidence = classify_exercise(lm)

            # Count exercises
            exercise_counts[exercise] = exercise_counts.get(exercise, 0) + 1

            # 2️⃣ Extract joints
            a, b, c = extract_landmarks(lm, exercise)

            if not a or not b or not c:
                results.append({
                    "file_name": file.filename,
                    "exercise": exercise,
                    "pose_detected": True,
                    "angle": None,
                    "feedback": "Unable to compute angle",
                    "performance_score": 0.0,
                    "rep_count": 0
                })
                continue

            # 3️⃣ Compute angle
            angle = calculate_angle(a, b, c)

            # 4️⃣ Get feedback and score
            feedback, score = evaluate_angle(exercise, angle)

            # 5️⃣ Rep estimation
            rep_count = 1 if score >= 0.8 else 0

            # Track performance
            total_score += score
            valid_count += 1

            results.append({
                "file_name": file.filename,
                "exercise": exercise,
                "confidence": round(confidence, 2),
                "pose_detected": True,
                "angle": round(angle, 2),
                "feedback": feedback,
                "performance_score": round(score, 2),
                "rep_count": rep_count
            })

    # Summary
    avg_score = round(total_score / valid_count, 2) if valid_count > 0 else 0.0
    most_common_exercise = max(exercise_counts, key=exercise_counts.get) if exercise_counts else "unknown"

    return {
        "total_images": len(files),
        "processed_images": valid_count,
        "average_score": avg_score,
        "most_common_exercise": most_common_exercise,
        "results": results
    }


@app.post("/analyze-batch", response_model=List[PoseResult])
async def analyze_batch(
        exercise_type: str = Form(...),
        files: List[UploadFile] = File(...)
):
    results = []

    with mp_pose.Pose(static_image_mode=True) as pose:
        for file in files:
            data = await file.read()
            np_arr = np.frombuffer(data, np.uint8)
            img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            if img is None:
                results.append(PoseResult(
                    file_name=file.filename,
                    exercise=exercise_type,
                    pose_detected=False,
                    angle=None,
                    feedback="Invalid image",
                    performance_score=0.0
                ))
                continue

            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            res = pose.process(img_rgb)

            if not res.pose_landmarks:
                results.append(PoseResult(
                    file_name=file.filename,
                    exercise=exercise_type,
                    pose_detected=False,
                    angle=None,
                    feedback="No person detected",
                    performance_score=0.0
                ))
                continue

            lm = res.pose_landmarks.landmark
            a, b, c = extract_landmarks(lm, exercise_type)

            if not a or not b or not c:
                results.append(PoseResult(
                    file_name=file.filename,
                    exercise=exercise_type,
                    pose_detected=False,
                    angle=None,
                    feedback="Invalid landmark selection for exercise",
                    performance_score=0.0
                ))
                continue

            angle = calculate_angle(a, b, c)
            feedback, score = evaluate_angle(exercise_type, angle)

            results.append(PoseResult(
                file_name=file.filename,
                exercise=exercise_type,
                pose_detected=True,
                angle=round(angle, 2),
                feedback=feedback,
                performance_score=round(score, 2)
            ))

    return results
