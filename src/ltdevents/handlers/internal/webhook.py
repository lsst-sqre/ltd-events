"""Handlers for the internal ``/webhook/`` endpoint."""

__all__ = ["post_webhook"]

import pydantic
from aiohttp import web

from ltdevents.handlers import internal_routes
from ltdevents.webhookmodels import parse_event


@internal_routes.post("/webhook")
async def post_webhook(request: web.Request) -> web.Response:
    """Handle ``POST /webhook`` (internal endpoint).

    This endpoint is the general purpose handler for all webhook payloads from
    LTD Keeper, and converts them into Kafka messages.

    Since this endpoint is only exposed to the internal Kubernetes network,
    we trust the payloads. The next step will be to add payload verification.
    """
    logger = request["safir/logger"]
    payload = await request.json()
    try:
        event = parse_event(payload=payload, logger=logger)
    except pydantic.ValidationError as e:
        logger.error("Validation error", info=e.json())
        return web.json_response({"error": e.json()}, status=400)
    except RuntimeError as e:
        logger.error("Validation error", info=str(e))
        return web.json_response({"error": str(e)}, status=400)

    logger.debug("Parsed webhook", webhookevent=event)

    return web.Response(status=200)
