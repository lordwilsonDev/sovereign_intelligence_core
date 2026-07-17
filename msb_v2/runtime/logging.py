from __future__ import annotations

import logging
import sys
from typing import Optional


def configure_logging(level: str = "info") -> None:
    """Idempotent stdlib logging bootstrap."""
    root = logging.getLogger()
    if root.handlers:
        return
    handler = logging.StreamHandler(sys.stdout)
    fmt = "%(asctime)s %(levelname)s %(name)s :: %(message)s"
    handler.setFormatter(logging.Formatter(fmt))
    root.addHandler(handler)
    root.setLevel(getattr(logging, str(level).upper(), logging.INFO))


def get_logger(name: Optional[str] = None) -> logging.Logger:
    return logging.getLogger(name)
