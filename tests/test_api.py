import pytest


def test_get_activities(client):
    """Test GET /activities returns all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert len(data) == 9


def test_get_activities_has_required_fields(client):
    """Test that each activity has required fields"""
    response = client.get("/activities")
    data = response.json()
    
    for activity_name, activity in data.items():
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity
        assert isinstance(activity["participants"], list)


def test_signup_for_activity(client):
    """Test POST /activities/{activity_name}/signup signs up a student"""
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "alice@mergington.edu"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "Signed up" in data["message"]
    assert "alice@mergington.edu" in data["message"]


def test_signup_adds_participant(client):
    """Test that signup actually adds participant to the activity"""
    client.post(
        "/activities/Chess Club/signup",
        params={"email": "alice@mergington.edu"}
    )
    
    response = client.get("/activities")
    activities = response.json()
    assert "alice@mergington.edu" in activities["Chess Club"]["participants"]
    assert len(activities["Chess Club"]["participants"]) == 3


def test_unregister_from_activity(client):
    """Test DELETE /activities/{activity_name}/unregister removes a student"""
    response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": "michael@mergington.edu"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "Removed" in data["message"]


def test_unregister_removes_participant(client):
    """Test that unregister actually removes participant from the activity"""
    client.delete(
        "/activities/Chess Club/unregister",
        params={"email": "michael@mergington.edu"}
    )
    
    response = client.get("/activities")
    activities = response.json()
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]
    assert len(activities["Chess Club"]["participants"]) == 1


def test_signup_then_unregister(client):
    """Test signup followed by unregister"""
    # Sign up
    client.post(
        "/activities/Chess Club/signup",
        params={"email": "bob@mergington.edu"}
    )
    
    # Verify signup
    response = client.get("/activities")
    activities = response.json()
    assert "bob@mergington.edu" in activities["Chess Club"]["participants"]
    assert len(activities["Chess Club"]["participants"]) == 3
    
    # Unregister
    client.delete(
        "/activities/Chess Club/unregister",
        params={"email": "bob@mergington.edu"}
    )
    
    # Verify unregister
    response = client.get("/activities")
    activities = response.json()
    assert "bob@mergington.edu" not in activities["Chess Club"]["participants"]
    assert len(activities["Chess Club"]["participants"]) == 2


def test_signup_for_nonexistent_activity(client):
    """Test signup for activity that doesn't exist"""
    response = client.post(
        "/activities/Nonexistent Club/signup",
        params={"email": "alice@mergington.edu"}
    )
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_from_nonexistent_activity(client):
    """Test unregister from activity that doesn't exist"""
    response = client.delete(
        "/activities/Nonexistent Club/unregister",
        params={"email": "alice@mergington.edu"}
    )
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
