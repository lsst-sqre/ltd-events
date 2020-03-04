"""Configuration definition."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

__all__ = ["Configuration"]


if TYPE_CHECKING:
    from typing import Optional


@dataclass
class Configuration:
    """Configuration for ltdevents."""

    name: str = os.getenv("SAFIR_NAME", "ltdevents")
    """The application's name, which doubles as the root HTTP endpoint path.

    Set with the ``SAFIR_NAME`` environment variable.
    """

    profile: str = os.getenv("SAFIR_PROFILE", "development")
    """Application run profile: "development" or "production".

    Set with the ``SAFIR_PROFILE`` environment variable.
    """

    logger_name: str = os.getenv("SAFIR_LOGGER", "ltdevents")
    """The root name of the application's logger.

    Set with the ``SAFIR_LOGGER`` environment variable.
    """

    log_level: str = os.getenv("SAFIR_LOG_LEVEL", "INFO")
    """The log level of the application's logger.

    Set with the ``SAFIR_LOG_LEVEL`` environment variable.
    """

    kafka_protocol: str = os.getenv("SAFIR_KAFKA_PROTOCOL", "SSL")
    """The protocol used for communicating with Kafka brokers: SSL or
    PLAINTEXT.

    Set with the ``SAFIR_KAFKA_PROTOCOL`` environment variable.
    """

    kafka_cluster_ca_path: Optional[Path] = field(
        default_factory=lambda: get_env_optional_path("SAFIR_KAFKA_CLUSTER_CA")
    )
    """The path of the Strimzi-generated SSL cluster CA file for the Kafka
    brokers.

    Set with the ``SAFIR_KAFKA_CLUSTER_CA`` environment variable.
    """

    kafka_client_ca_path: Optional[Path] = field(
        default_factory=lambda: get_env_optional_path("SAFIR_KAFKA_CLIENT_CA")
    )
    """The path of the Strimzi-generated SSL client CA file for the Kafka
    client.

    Set with the ``SAFIR_KAFKA_CLIENT_CA`` environment variable.
    """

    kafka_client_cert_path: Optional[Path] = field(
        default_factory=lambda: get_env_optional_path(
            "SAFIR_KAFKA_CLIENT_CERT"
        )
    )
    """The path of the Strimzi-generated SSL cluster cert file for the Kafka
    client.

    Set with the ``SAFIR_KAFKA_CLIENT_CERT`` environment variable.
    """

    kafka_client_key_path: Optional[Path] = field(
        default_factory=lambda: get_env_optional_path("SAFIR_KAFKA_CLIENT_KEY")
    )
    """The path of the Strimzi-generated SSL client key file for the Kafka
    client.

    Set with the ``SAFIR_KAFKA_CLIENT_KEY`` environment variable.
    """


def get_env_optional_path(envvar: str) -> Optional[Path]:
    """Get a path from an environment variable, falling back if it does not
    exist.

    Use this function in conjunction with ``default_factory`` for configuration
    dataclasses.

    Parameters
    ----------
    envvar : `str`
        Name of an environment variable.

    Returns
    -------
    value : `Path` or `None`
        A `pathlib.Path` for the environment variable's value, or `None` if the
        environment variable is not set.
    """
    value = os.getenv(envvar)
    if value is None:
        return None
    else:
        return Path(value)
