from fastapi.testclient import TestClient
from src.app import app


client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # Expect some known activity to be present
    assert "Basketball Team" in data


def test_signup_and_unregister_flow():
    activity = "Basketball Team"
    email = "testuser@example.com"

    # Ensure email is not already present
    resp = client.get("/activities")
    participants = resp.json().get(activity, {}).get("participants", [])
    if email in participants:
        # remove if present to ensure test isolation
        client.post(f"/activities/{activity}/unregister?email={email}")

    # Sign up
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert "Signed up" in resp.json().get("message", "")

    # Verify participant was added
    resp = client.get("/activities")
    participants = resp.json().get(activity, {}).get("participants", [])
    assert email in participants

    # Unregister
    resp = client.post(f"/activities/{activity}/unregister?email={email}")
    assert resp.status_code == 200
    assert "Unregistered" in resp.json().get("message", "")

    # Verify participant was removed
    resp = client.get("/activities")
    participants = resp.json().get(activity, {}).get("participants", [])
    assert email not in participants
