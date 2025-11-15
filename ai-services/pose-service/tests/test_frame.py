from starlette.testclient import TestClient
from unittest.mock import patch, MagicMock
from ..app.main import app


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
def test_frame_analysis(mock_exit, mock_enter, mock_process):

    # mock entering context
    mock_enter.return_value = MagicMock()
    mock_process.return_value.pose_landmarks = MagicMock(
        landmark=fake_landmarks()
    )

    # create fake JPEG file
    file_bytes = b"\xff\xd8\xff\xdb\x00\x43\x00"  # minimal jpeg header

    response = client.post(
        "/workouts/frame",
        files={"file": ("test.jpg", file_bytes, "image/jpeg")}
    )

    assert response.status_code == 200
    result = response.json()
    assert result["pose_detected"] is True
    assert "exercise" in result
    assert "angle" in result
