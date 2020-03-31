"""Models for webhook payloads from LTD Keeper that are recieved by the
``post_webhook`` endpoint.
"""

from __future__ import annotations

import datetime
from typing import Any, Dict

from pydantic import BaseModel, HttpUrl

__all__ = ["parse_event", "EditionUpdatedEvent"]


def parse_event(payload: Dict[str, Any], logger: Any) -> BaseEvent:
    """Parse a webhook payload (automatically sorting its event type).

    Parameters
    ----------
    payload : `dict`
        The webhook payload body, parsed from JSON.
    logger
        Structlog logger instance.

    Returns
    -------
    pydantic.BaseEvent
        The parsed payload, depending on the webhook event type:

        edition.updated
            `EditionUpdatedEvent`
    """
    try:
        event_type = payload["event_type"]
    except KeyError:
        raise RuntimeError("Payload does not contain ``event_type``.")

    if event_type == "edition.updated":
        event = EditionUpdatedEvent.parse_obj(payload)
    else:
        raise RuntimeError(f"Payload type ``{event_type}`` is not known.")

    return event


class ProductInfo(BaseModel):
    """A model for information about an LSST the Docs product.

    This model appears within webhook payload models.
    """

    url: HttpUrl

    published_url: HttpUrl

    title: str

    slug: str


class EditionInfo(BaseModel):
    """A model for information about an edition.

    This model appears within webhook payload models.
    """

    url: HttpUrl
    """The LTD Keeper API URL of the edition resource."""

    published_url: HttpUrl
    """The website URL of the edition."""

    title: str
    """The title of the edition."""

    slug: str
    """The LTD Keeper API slug of the edition resource."""

    build_url: HttpUrl
    """The LTD Keeper API URL of the edition's build resource."""


class BaseEvent(BaseModel):
    """A baseclass for webhook payload models."""

    event_type: str = "edition.updated"
    """Name of the event."""

    event_timestamp: datetime.datetime
    """Timestamp when the event happened."""


class EditionUpdatedEvent(BaseEvent):
    """A webhook payload model for edition.updated events."""

    edition: EditionInfo
    """Information about the edition that was updated."""

    product: ProductInfo
    """Information about the edition's product resource."""
