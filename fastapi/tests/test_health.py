from testclient import TestClient
from app.main import create_app

client = TestClient(create_app())

def test_app_root():
    response = client.get("/")
    assert response.status_code == 200
