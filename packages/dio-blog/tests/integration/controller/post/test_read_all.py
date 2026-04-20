import pytest
import pytest_asyncio
from datetime import datetime

from fastapi import status
from httpx import AsyncClient

@pytest_asyncio.fixture(autouse=True)
async def populate_posts(db):
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

@pytest.mark.parametrize("published,total", [("on", 2), ("off", 1)])
async def test_read_posts_by_status_success(client: AsyncClient, 
                                            access_token: str, 
                                            published: str, 
                                            total: int):
    # given
    params = {"published": published, "limit": 10, "skip": 0}
    headers = {"Authorization": f"Bearer {access_token}"}

    # when
    response = await client.get("/posts", params=params, headers=headers)

    # then
    content = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(content) == total

async def test_read_posts_limit_success(client: AsyncClient, access_token: str):
    # given
    params = {"published": "on", "limit": 1, "skip": 0}
    headers = {"Authorization": f"Bearer {access_token}"}

    # when
    response = await client.get("/posts", params=params, headers=headers)

    # then
    content = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(content) == 1

async def test_read_posts_not_authenticated_fail(client: AsyncClient):
    # given
    params = {"published": "on", "limit": 10, "skip": 0}

    # when
    response = await client.get("/posts", params=params, headers={})

    # then
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

async def test_read_posts_empty_parameters_fail(client: AsyncClient, access_token: str):
    # given
    headers = {"Authorization": f"Bearer {access_token}"}

    # when
    response = await client.get("/posts", params={}, headers=headers)

    # then
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
