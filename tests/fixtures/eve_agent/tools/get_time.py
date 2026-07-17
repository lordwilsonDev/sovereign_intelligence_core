import time

def get_time(**_: dict) -> dict:
    """Return current local time as a string."""
    return {"status": "ok", "message": time.strftime("%Y-%m-%d %H:%M:%S"), "confidence": 1.0}
