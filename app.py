"""Flask application with logging to stderr."""

import logging

from flask import Flask, jsonify

from logging_config import configure_logging

app = Flask(__name__)
configure_logging(app)

logger = logging.getLogger(__name__)

@app.route("/")
def hello_world():
    """Return a hello world message."""
    logger.info("Hello world endpoint was called")
    return jsonify({"message": "Hello, World!"})

@app.route("/health")
def health_check():
    """Return application health status."""
    logger.info("Health check endpoint was called")
    return jsonify({"status": "healthy"}), 200

@app.route("/error")
def trigger_error():
    """Trigger a dummy error for testing error logging."""
    logger.error("Dummy error endpoint was called")
    try:
        raise RuntimeError("This is a dummy error")
    except RuntimeError:
        logger.exception("An unexpected dummy error occurred")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route("/client-error")
def trigger_client_error():
    """Trigger a dummy client error for testing error logging."""
    logger.warning("Dummy client error endpoint was called")
    return jsonify({"error": "Bad user request"}), 400

@app.route("/uncaught-error")
def trigger_uncaught_error():
    """Trigger an uncaught error for testing error logging."""
    logger.info("Uncaught error endpoint was called")
    # This will raise a ZeroDivisionError, which is uncaught
    result = 1 / 0
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
