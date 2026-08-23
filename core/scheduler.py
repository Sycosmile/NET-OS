"""Runs the engine on a fixed interval, either once or in a loop."""

import time
import logging

from core.engine import run_engine

logger = logging.getLogger("netos.scheduler")


def tick() -> dict:
    """Run a single engine tick and return its result."""
    result = run_engine()
    logger.info(
        "tick: health=%s strategy=%s",
        result["health"]["overall"],
        result["strategy"]["strategy"],
    )
    return result


def run_loop(interval: float = 5.0, stop_event=None):
    """Run tick() repeatedly every `interval` seconds.

    If `stop_event` (a threading.Event) is provided, the loop exits
    cleanly once it's set — used by the daemon for graceful shutdown.
    """
    logger.info("scheduler loop starting (interval=%ss)", interval)
    while stop_event is None or not stop_event.is_set():
        tick()
        time.sleep(interval)
