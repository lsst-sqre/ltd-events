"""Handlers for the internal ``/webhook/`` endpoint."""

__all__ = ["post_webhook"]

import pydantic
from aiohttp import web

from ltdevents.handlers import internal_routes
from ltdevents.webhookmodels import EditionUpdatedEvent, parse_event


@internal_routes.post("/webhook")
async def post_webhook(request: web.Request) -> web.Response:
    """Handle ``POST /webhook`` (internal endpoint).

    This endpoint is the general purpose handler for all webhook payloads from
    LTD Keeper, and converts them into Kafka messages.

    Since this endpoint is only exposed to the internal Kubernetes network,
    we trust the payloads. The next step will be to add payload verification.
    """
    logger = request["safir/logger"]
    logger.debug("New webhook event")
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

    producer = request.config_dict["safir/kafka_producer"]
    schema_manager = request.config_dict["safir/schema_manager"]
    kafka_topic = request.config_dict["safir/config"].events_kafka_topic

    if event.event_type == "edition.updated":
        assert isinstance(event, EditionUpdatedEvent)

        key_bytes = await schema_manager.serialize(
            data={
                "product_slug": event.product.slug,
                "edition_slug": event.edition.slug,
            },
            name="ltd.edition_key_v1",
        )
        value_bytes = await schema_manager.serialize(
            data=event.dict(), name="ltd.edition_update_v1"
        )

        await producer.send_and_wait(
            kafka_topic, key=key_bytes, value=value_bytes
        )
        logger.debug(
            "Sent Kafka message",
            event_type="edition.updated",
            product=event.product.slug,
            edition=event.edition.slug,
        )

    return web.Response(status=200)
