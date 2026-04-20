from fastapi import status
from httpx import AsyncClient

async def test_create_post_success(client: AsyncClient, access_token: str):
    # given
    data = {"title": "post 1", 
            "content": "This is a test post.",
            "published_at": "2025-06-01T12:23:44.201Z",
            "published": True}
    headers = {"Authorization": f"Bearer {access_token}"}

    # when
    response = await client.post("/posts", json=data, headers=headers)

    # then
    content = response.json()
    assert response.status_code == status.HTTP_201_CREATED
    assert content["id"] is not None

async def test_create_post_invalid_payload_fail(client: AsyncClient, access_token: str):
    # given
    data = {"content": "This is a test post.",
            "published_at": "2025-06-01T12:23:44.201Z",
            "published": True}
    headers = {"Authorization": f"Bearer {access_token}"}

    # when
    response = await client.post("/posts", json=data, headers=headers)

    # then
    content = response.json()

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert content["detail"][0]["loc"] == ["body", "title"]

async def test_create_post_not_authenticated_fail(client: AsyncClient):
    # given
    data = {"title": "post 1", 
            "content": "This is a test post.",
            "published_at": "2025-06-01T12:23:44.201Z",
            "published": True}

    # when
    response = await client.post("/posts", json=data, headers={})

    # then
    content = response.json()

    assert response.status_code == status.HTTP_401_UNAUTHORIZED