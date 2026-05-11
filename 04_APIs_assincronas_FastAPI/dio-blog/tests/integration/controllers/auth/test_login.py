from fastapi import status
from httpx import AsyncClient


async def test_login_success(client: AsyncClient):
    # Given
    data = {"user_id": 1}

    # When
    response = await client.post("/login", json={"user_id": 1})

    token = response.json()["access_token"]

    # Then
    assert response.status_code == status.HTTP_200_OK
    assert token is not None
