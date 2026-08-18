from fastapi.testclient import TestClient

from app.main import app


def test_login_and_me() -> None:
    with TestClient(app) as client:
        login_response = client.post(
            "/api/v1/auth/login",
            data={
                "username": "admin@example.com",
                "password": "Admin@123",
            },
        )

        assert login_response.status_code == 200

        token = login_response.json()["access_token"]

        me_response = client.get(
            "/api/v1/auth/me",
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        assert me_response.status_code == 200
        assert me_response.json()["email"] == "admin@example.com"

