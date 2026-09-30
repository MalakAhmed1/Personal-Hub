from fastapi.testclient import TestClient
from personal_hub.main import app

client = TestClient(app)

def test_status_endpoint():
    response = client.get("/hub/meeting-notes/")
    assert response.status_code == 200
    assert response.json() == {"status": "meeting notes module is alive"}

# def test_analyze_meeting_notes():
#     response = client.post("/hub/meeting-notes/", json={"notes": "Decision: Implement user authentication. Action Item: Create login page. Follow-up Question: What are the security requirements?"})
#     assert response.status_code == 200
#     assert "decisions" in response.json()
#     assert "action_items" in response.json()
#     assert "follow_up_questions" in response.json()