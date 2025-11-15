from starlette.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app



client = TestClient(app)

def fake_landmarks():
    class LM:
        def __init__(self, x=0.5, y=0.5):
            self.x = x
            self.y = y
    return [LM() for _ in range(33)]

@patch("app.main.mp_pose.Pose.process")
@patch("app.main.mp_pose.Pose.__enter__")
@patch("app.main.mp_pose.Pose.__exit__")
def test_batch_analysis(mock_exit, mock_enter, mock_process):

    mock_enter.return_value = MagicMock()
    mock_process.return_value.pose_landmarks = MagicMock(
        landmark=fake_landmarks()
    )

    files = [
        ("files", ("img1.jpg", b"\xff\xd8\xff", "image/jpeg")),
        ("files", ("img2.jpg", b"\xff\xd8\xff", "image/jpeg")),
    ]

    response = client.post("/workouts/batch", files=files)
    assert response.status_code == 200
    data = response.json()

    assert data["total_images"] == 2
    assert len(data["results"]) == 2
