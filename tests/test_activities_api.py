import urllib.parse
from src.app import activities


def test_get_activities_returns_all(client):
    # Arrange: client fixture provides TestClient
    # Act
    resp = client.get("/activities")
    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert len(data) == len(activities)


def test_signup_new_student_success(client):
    # Arrange
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    # Act
    resp = client.post(f"/activities/{urllib.parse.quote(activity)}/signup", params={"email": email})
    # Assert
    assert resp.status_code == 200
    assert "Signed up" in resp.json().get("message", "")
    all_activities = client.get("/activities").json()
    assert email in all_activities[activity]["participants"]


def test_signup_duplicate_email_returns_400(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"  # pre-seeded
    # Act
    resp = client.post(f"/activities/{urllib.parse.quote(activity)}/signup", params={"email": email})
    # Assert
    assert resp.status_code == 400
    assert "already signed up" in resp.json().get("detail", "").lower()


def test_signup_nonexistent_activity_returns_404(client):
    # Arrange
    activity = "Nonexistent Club"
    email = "someone@mergington.edu"
    # Act
    resp = client.post(f"/activities/{urllib.parse.quote(activity)}/signup", params={"email": email})
    # Assert
    assert resp.status_code == 404
    assert "not found" in resp.json().get("detail", "").lower()


def test_unregister_existing_student_success(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"
    # Act
    resp = client.delete(f"/activities/{urllib.parse.quote(activity)}/unregister", params={"email": email})
    # Assert
    assert resp.status_code == 200
    assert "Unregistered" in resp.json().get("message", "")
    all_activities = client.get("/activities").json()
    assert email not in all_activities[activity]["participants"]


def test_unregister_not_signed_up_returns_400(client):
    # Arrange
    activity = "Chess Club"
    email = "notregistered@mergington.edu"
    # Act
    resp = client.delete(f"/activities/{urllib.parse.quote(activity)}/unregister", params={"email": email})
    # Assert
    assert resp.status_code == 400
    assert "not signed up" in resp.json().get("detail", "").lower()


def test_unregister_nonexistent_activity_returns_404(client):
    # Arrange
    activity = "NoSuchActivity"
    email = "michael@mergington.edu"
    # Act
    resp = client.delete(f"/activities/{urllib.parse.quote(activity)}/unregister", params={"email": email})
    # Assert
    assert resp.status_code == 404
    assert "not found" in resp.json().get("detail", "").lower()


def test_root_redirects_to_static(client):
    # Arrange
    # Act
    resp = client.get("/", follow_redirects=False)
    # Assert
    assert resp.status_code in (301, 302, 307, 308)
    assert "/static/index.html" in resp.headers.get("location", "")
