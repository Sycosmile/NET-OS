"""Runs the scheduler loop in a background thread alongside the API."""

import threading
import logging

from core.scheduler import run_loop

logger = logging.getLogger("netos.daemon")

_stop_event = threading.Event()
_thread = None


def start_daemon(interval: float = 5.0):
    """Start the scheduler loop in a background daemon thread.

    Safe to call once at app startup. Returns the thread object so
    callers can join() on it if needed (mainly for tests).
    """
    global _thread
    if _thread is not None and _thread.is_alive():
        logger.warning("daemon already running, ignoring start request")
        return _thread

    _stop_event.clear()
    _thread = threading.Thread(
        target=run_loop,
        kwargs={"interval": interval, "stop_event": _stop_event},
        daemon=True,
        name="netos-scheduler",
    )
    _thread.start()
    logger.info("daemon started (interval=%ss)", interval)
    return _thread


def stop_daemon():
    """Signal the background loop to stop after its current sleep."""
    _stop_event.set()
    logger.info("daemon stop requested")
