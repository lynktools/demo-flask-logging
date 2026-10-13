# Python JSON-Logging Flask Demo

A minimal Flask application that demonstrates structured JSON logging to `stderr`, served with Gunicorn.

## Features

- Three HTTP endpoints: `Hello World`, `Health Check`, and `Trigger Error`
- Flask logging configured via `dictConfig` in `logging_config.py`
- JSON log format with timestamp (UTC ISO 8601), PID, level, app name, HTTP method, path, endpoint, client IP, message, and traceback
- Gunicorn configuration in `gunicorn.conf.py`

## Requirements

- Python 3.12+
- Flask
- Gunicorn

## Installation

```bash
pip install -r requirements.txt
```

## Running the Application

```bash
gunicorn --config gunicorn.conf.py app:app
```

The application will be available at `http://localhost:8000`.

## Logging

- Application logs are emitted as JSON to `stderr`.
- Each route triggers its own log line.
- Request context (HTTP method, path, endpoint, client IP) is injected into every application log via a custom `RequestContextFilter`.
- Gunicorn access logs are disabled (`accesslog = None`) to avoid duplicate request logging.
- Gunicorn error logs (startup, worker, shutdown) remain enabled on `stderr`.
- By default, the application logs at `INFO` level and above. You can adjust these levels via environment variables:

```bash
APP_LOG_LEVEL=DEBUG ROOT_LOG_LEVEL=ERROR gunicorn --config gunicorn.conf.py app:app
```

## Endpoints

| Endpoint          | Method | Description                                                         |
| ----------------- | ------ | ------------------------------------------------------------------- |
| `/`               | GET    | Returns `{"message": "Hello, World!"}`                              |
| `/health`         | GET    | Returns `{"status": "healthy"}`                                     |
| `/error`          | GET    | Triggers a dummy error and returns 500                              |
| `/client-error`   | GET    | Triggers a dummy client error and returns 400                       |
| `/uncaught-error` | GET    | Triggers an uncaught error (e.g. ZeroDivisionError) and returns 500 |

## Example Log Output

```jsonl
{"timestamp": "2026-10-05T04:53:57.475683+00:00", "level": "INFO", "app": "app", "pid": 6039, "message": "Health check endpoint was called", "method": "GET", "path": "/health", "endpoint": "health_check", "client_ip": "127.0.0.1"}
{"timestamp": "2026-10-05T04:54:01.406972+00:00", "level": "WARNING", "app": "app", "pid": 6039, "message": "Dummy client error endpoint was called", "method": "GET", "path": "/client-error", "endpoint": "trigger_client_error", "client_ip": "127.0.0.1"}
{"timestamp": "2026-10-05T04:54:07.679285+00:00", "level": "ERROR", "app": "app", "pid": 6039, "message": "Dummy error endpoint was called", "method": "GET", "path": "/error", "endpoint": "trigger_error", "client_ip": "127.0.0.1"}
{"timestamp": "2026-10-05T04:54:07.679493+00:00", "level": "ERROR", "app": "app", "pid": 6039, "message": "An unexpected dummy error occurred", "method": "GET", "path": "/error", "endpoint": "trigger_error", "client_ip": "127.0.0.1", "traceback": ["Traceback (most recent call last):\n", "  File \"/home/luki/projects/lynk/lynk-demo-app-logging/app.py\", line 34, in trigger_error\n    raise RuntimeError(\"This is a dummy error\")\n", "RuntimeError: This is a dummy error\n"]}
```

## Project Structure

```
.
├── app.py              # Flask application
├── logging_config.py   # Logging configuration (dictConfig + JSON formatter)
├── gunicorn.conf.py    # Gunicorn configuration
├── requirements.txt    # Python dependencies
├── .gitignore          # Git ignore rules
└── README.md           # Project documentation
```

## References

- [Logging - Lynk Wiki](https://wiki.kodingua.com/guide/logging)
