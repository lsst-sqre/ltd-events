"""The main application definition for ltdevents service."""

from __future__ import annotations

from pathlib import Path
from typing import AsyncGenerator

import structlog
from aiohttp import web
from kafkit.registry.aiohttp import RegistryApi
from kafkit.registry.manager import RecordNameSchemaManager
from safir.events import configure_kafka_ssl, init_kafka_producer
from safir.http import init_http_session
from safir.logging import configure_logging
from safir.metadata import setup_metadata
from safir.middleware import bind_logger

from ltdevents.config import Configuration
from ltdevents.handlers import init_external_routes, init_internal_routes

__all__ = ["create_app"]


def create_app() -> web.Application:
    """Create and configure the aiohttp.web application."""
    config = Configuration()
    configure_logging(
        profile=config.profile,
        log_level=config.log_level,
        name=config.logger_name,
    )

    root_app = web.Application()
    root_app["safir/config"] = config
    setup_metadata(package_name="ltd-events", app=root_app)
    setup_middleware(root_app)
    root_app.add_routes(init_internal_routes())
    root_app.cleanup_ctx.append(init_http_session)
    root_app.cleanup_ctx.append(configure_kafka_ssl)
    root_app.cleanup_ctx.append(init_avro_serializers)
    root_app.cleanup_ctx.append(init_kafka_producer)

    sub_app = web.Application()
    setup_middleware(sub_app)
    sub_app.add_routes(init_external_routes())
    root_app.add_subapp(f'/{root_app["safir/config"].name}', sub_app)

    return root_app


def setup_middleware(app: web.Application) -> None:
    """Add middleware to the application."""
    app.middlewares.append(bind_logger)


async def init_avro_serializers(app: web.Application) -> AsyncGenerator:
    """Initialize Avro serializers."""
    logger = structlog.get_logger(app["safir/config"].logger_name)

    registry_url = app["safir/config"].schema_registry_url
    if registry_url is None:
        logger.info(
            "Schema Registry is not configured, skipping schema "
            "registration"
        )
        app["safir/schema_registry"] = None
        app["safir/schema_manager"] = None

    else:
        registry = RegistryApi(
            session=app["safir/http_session"],
            url=app["safir/config"].schema_registry_url,
        )

        schema_root_dir = Path(__file__).parent / "schemas"

        manager = RecordNameSchemaManager(
            root=schema_root_dir,
            suffix=app["safir/config"].schema_suffix,
            registry=registry,
        )
        await manager.register_schemas(
            compatibility=app["safir/config"].schema_compatibility
        )

        app["safir/schema_registry"] = registry
        app["safir/schema_manager"] = manager
        logger.info("Finished registering Avro schemas")

    yield
