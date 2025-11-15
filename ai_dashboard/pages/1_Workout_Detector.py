import sys
import os

# Add project root to PYTHONPATH
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)


import streamlit as st
from ai_dashboard.services.pose_api import analyze_pose

st.title("🏋️ Workout Detector")
st.write("Upload one or multiple images to detect exercise type and receive feedback.")

# Select Exercise Type
exercise_type = st.selectbox(
    "Choose Exercise Type",
    ["squat", "pushup", "plank", "lunge", "bicep_curl"]
)

# File uploader
uploaded_files = st.file_uploader(
    "Upload workout images",
    type=["jpg", "png", "jpeg"],
    accept_multiple_files=True
)

# Analyze button
if st.button("Analyze"):
    if not uploaded_files:
        st.warning("Please upload at least one image.")
    else:
        st.write("Analyzing images...")
        results = []

        for file in uploaded_files:
            results.append(analyze_pose(file, exercise_type))

        st.success("Analysis Completed!")

        for r in results:
            st.subheader(r["file_name"])
            st.write(f"**Exercise:** {r['exercise']}")
            st.write(f"**Angle:** {r['angle']}")
            st.write(f"**Feedback:** {r['feedback']}")
            st.write(f"**Score:** {r['performance_score']}")
            st.write("---")
