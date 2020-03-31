"""Tests for the POST /webhook endpoint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ltdevents.app import create_app

if TYPE_CHECKING:
    from aiohttp.pytest_plugin.test_utils import TestClient


async def test_post_webhook_edition_updated(
    aiohttp_client: TestClient,
) -> None:
    """Test POST /webhook for an edition.updated event."""
    app = create_app()
    client = await aiohttp_client(app)

    payload = {
        "event_type": "edition.updated",
        "event_timestamp": "2020-01-01T12:00:00Z",
        "product": {
            "published_url": "https://example.lsst.io/",
            "url": "https://keeper.lsst.codes/products/example",
            "title": "Example product",
            "slug": "example",
        },
        "edition": {
            "published_url": "https://example.lsst.io/v/1.0",
            "url": "https://keeper.lsst.codes/editions/1234",
            "title": "Version 1.0",
            "slug": "1.0",
            "build_url": "https://keeper.lsst.codes/builds/1",
        },
    }

    response = await client.post("/webhook", json=payload)
    assert response.status == 200


async def test_post_webhook_unknown_type(aiohttp_client: TestClient) -> None:
    """Test POST /webhook for an unknown type of event."""
    app = create_app()
    client = await aiohttp_client(app)

    payload = {
        "event_type": "edition.nonexistent",
        "event_timestamp": "2020-01-01T12:00:00Z",
        "product": {
            "published_url": "https://example.lsst.io/",
            "url": "https://keeper.lsst.codes/products/example",
            "title": "Example product",
            "slug": "example",
        },
        "edition": {
            "published_url": "https://example.lsst.io/v/1.0",
            "url": "https://keeper.lsst.codes/editions/1234",
            "title": "Version 1.0",
            "slug": "1.0",
            "build_url": "https://keeper.lsst.codes/builds/1",
        },
    }

    response = await client.post("/webhook", json=payload)
    assert response.status == 400
    response_json = await response.json()
    assert "error" in response_json


async def test_post_webhook_missing_type(aiohttp_client: TestClient) -> None:
    """Test POST /webhook for an missing event_type field."""
    app = create_app()
    client = await aiohttp_client(app)

    payload = {
        "event_timestamp": "2020-01-01T12:00:00Z",
        "product": {
            "published_url": "https://example.lsst.io/",
            "url": "https://keeper.lsst.codes/products/example",
            "title": "Example product",
            "slug": "example",
        },
        "edition": {
            "published_url": "https://example.lsst.io/v/1.0",
            "url": "https://keeper.lsst.codes/editions/1234",
            "title": "Version 1.0",
            "slug": "1.0",
            "build_url": "https://keeper.lsst.codes/builds/1",
        },
    }

    response = await client.post("/webhook", json=payload)
    assert response.status == 400
    response_json = await response.json()
    assert "error" in response_json


async def test_post_webhook_edition_updated_invalid(
    aiohttp_client: TestClient,
) -> None:
    """Test POST /webhook for a invalid payload."""
    app = create_app()
    client = await aiohttp_client(app)

    payload = {
        "event_type": "edition.updated",
        "event_timestamp": "2020-01-01",
        "product": {
            "published_url": "https://example.lsst.io/",
            "url": "https://keeper.lsst.codes/products/example",
            "title": "Example product",
            "slug": "example",
        },
        "edition": {
            "published_url": "https://example.lsst.io/v/1.0",
            "url": "https://keeper.lsst.codes/editions/1234",
            "title": "Version 1.0",
            "slug": "1.0",
            "build_url": "https://keeper.lsst.codes/builds/1",
        },
    }

    response = await client.post("/webhook", json=payload)
    assert response.status == 400
    response_json = await response.json()
    assert "error" in response_json
