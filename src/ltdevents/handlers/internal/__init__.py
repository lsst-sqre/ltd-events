"""Internal HTTP handlers that serve relative to the root path, ``/``.

These handlers aren't externally visible since the app is available at a path,
``/ltdevents``. See `ltdevents.handlers.external` for
the external endpoint handlers.
"""

__all__ = ["get_index", "post_webhook"]

from ltdevents.handlers.internal.index import get_index
from ltdevents.handlers.internal.webhook import post_webhook
