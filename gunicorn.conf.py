"""Gunicorn configuration file."""

import logging
import sys

# Server socket
bind = "0.0.0.0:8000"

# Worker processes
workers = 2
worker_class = "sync"

# Logging
capture_output = True
accesslog = None  # Disable Gunicorn access logs
errorlog = "-"  # Log errors to stderr
loglevel = "info"


def on_starting(server):
    """Hook that runs before the master process is initialized."""
    print("Gunicorn is starting...", file=sys.stderr)


def on_exit(server):
    """Hook that runs just before exiting Gunicorn."""
    print("Gunicorn is shutting down...", file=sys.stderr)
