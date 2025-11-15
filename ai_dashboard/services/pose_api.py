import requests
from ai_dashboard.config import POSE_SERVICE_URL

def analyze_pose(uploaded_file, exercise_type):
    """
    uploaded_file = Streamlit UploadedFile object
    """

    file_bytes = uploaded_file.read()

    files = {
        "files": (uploaded_file.name, file_bytes, uploaded_file.type)
    }

    data = {"exercise_type": exercise_type}

    response = requests.post(
        f"{POSE_SERVICE_URL}/analyze-batch",
        files=files,
        data=data
    )

    # Streamlit requires resetting file buffer after read()
    uploaded_file.seek(0)

    return response.json()[0]
