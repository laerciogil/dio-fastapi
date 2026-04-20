import pytest_asyncio
from fastapi import status
from httpx import AsyncClient
from datetime import datetime

@pytest_asyncio.fixture(autouse=True)
async def populate_post(db):
    from dio_blog.schemas.post import PostRequest
    from dio_blog.service.post import PostService

    service = PostService()
    await service.create(PostRequest(
        title="post 1",
        content="This is the first test post.",
        published_at=datetime.fromisoformat("2025-06-05T10:15:12.555Z"),
        published=True
    ))
    await service.create(PostRequest(
        title="post 2",
        content="This is the second test post.",
        published=False
    ))
    await service.create(PostRequest(
        title="post 3",
        content="This is the third test post.",
        published_at=datetime.fromisoformat("2025-07-01T12:23:44.201Z"),
        published=True
    ))

async def test_delete_post_success(client: AsyncClient, access_token: str):
    # given
    post_id = 1
    headers = {"Authorization": f"Bearer {access_token}"}

    # when
    response = await client.delete(f"/posts/{post_id}", headers=headers)

    # then
    assert response.status_code == status.HTTP_204_NO_CONTENT

async def test_delete_post_not_authenticated_fail(client: AsyncClient):
    # given
    post_id = 1

    # when
    response = await client.delete(f"/posts/{post_id}", headers={})

    # then
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

async def test_read_post_not_found_fail(client: AsyncClient, access_token: str):
    # given
    post_id = 99999999
    headers = {"Authorization": f"Bearer {access_token}"}

    # when
    response = await client.delete(f"/posts/{post_id}", headers=headers)

    # then
    assert response.status_code == status.HTTP_204_NO_CONTENT