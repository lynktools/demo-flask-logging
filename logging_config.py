"""Flask logging configuration using dictConfig with JSON formatting."""

import json
import logging
import os
import traceback
from datetime import datetime, timezone
from logging.config import dictConfig

from flask import has_request_context, request

APP_LOG_LEVEL = os.environ.get("APP_LOG_LEVEL", "INFO").upper()
ROOT_LOG_LEVEL = os.environ.get("ROOT_LOG_LEVEL", "INFO").upper()

class RequestContextFilter(logging.Filter):
    """Inject Flask request context into log records."""

    def filter(self, record: logging.LogRecord) -> bool:
        if has_request_context():
            record.method = request.method
            record.path = request.path
            record.endpoint = request.endpoint or "unknown"
            # Prefer the first address in the access route to support proxies.
            record.client_ip = (
                request.access_route[0] if request.access_route else request.remote_addr
            )
        else:
            record.method = None
            record.path = None
            record.endpoint = None
            record.client_ip = None
        return True


class JsonFormatter(logging.Formatter):
    """Emit log records as JSON objects."""

    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "app": record.name,
            "pid": os.getpid(),
            "message": record.getMessage(),
        }

        optional_fields = {
            "method": getattr(record, "method", None),
            "path": getattr(record, "path", None),
            "endpoint": getattr(record, "endpoint", None),
            "client_ip": getattr(record, "client_ip", None),
        }
        for key, value in optional_fields.items():
            if value is not None:
                log_entry[key] = value

        if record.exc_info:
            log_entry["traceback"] = traceback.format_exception(*record.exc_info)

        return json.dumps(log_entry, default=str)


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": "logging_config.JsonFormatter",
        },
    },
    "filters": {
        "request_context": {
            "()": "logging_config.RequestContextFilter",
        },
    },
    "handlers": {
        "stderr": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
            "formatter": "json",
            "level": "DEBUG",
            "filters": ["request_context"],
        },
    },
    "loggers": {
        "app": {
            "handlers": ["stderr"],
            "level": APP_LOG_LEVEL,
            "propagate": False,
        },
    },
    "root": {
        "handlers": ["stderr"],
        "level": ROOT_LOG_LEVEL,
    },
}


def configure_logging(app):
    """Configure Flask logging to output JSON logs to stderr using dictConfig."""
    dictConfig(LOGGING_CONFIG)
    # Ensure Flask's app logger uses the configured "app" logger settings.
    app.logger.name = "app"
