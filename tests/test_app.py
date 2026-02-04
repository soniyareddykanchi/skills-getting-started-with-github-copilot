from pathlib import Path
import sys

# Ensure src is importable
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from fastapi.testclient import TestClient
from app import app, activities

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # Check a known activity exists
    assert "Basketball Team" in data


def test_signup_and_unregister():
    activity = "Programming Class"
    test_email = "tester@example.com"

    # Snapshot initial participants to restore after test
    initial = list(activities[activity]["participants"])
    try:
        # Sign up
        r = client.post(f"/activities/{activity}/signup?email={test_email}")
        assert r.status_code == 200
        assert test_email in activities[activity]["participants"]

        # Unregister
        r2 = client.delete(f"/activities/{activity}/participants?email={test_email}")
        assert r2.status_code == 200
        assert test_email not in activities[activity]["participants"]

    finally:
        # Restore original state
        activities[activity]["participants"] = initial
