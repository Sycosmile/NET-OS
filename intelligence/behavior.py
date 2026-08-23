"""Flags anomalous current metrics against a rolling historical baseline."""

import statistics

from memory.db import fetch_recent_metrics
from intelligence.health import collect_metrics

STD_DEV_THRESHOLD = 2.0


def analyze_behavior(history_limit: int = 20) -> dict:
    """Compare the current reading to the recent historical baseline.

    Flags "anomalous" if CPU or memory is more than STD_DEV_THRESHOLD
    standard deviations away from the mean of recent history — a
    standard, lightweight anomaly-detection approach.
    """
    history = fetch_recent_metrics(limit=history_limit)
    current = collect_metrics()

    if len(history) < 5:
        return {
            "behavior": "insufficient_data",
            "samples": len(history),
        }

    cpu_values = [r["cpu_percent"] for r in history]
    mem_values = [r["memory_percent"] for r in history]

    cpu_mean = statistics.mean(cpu_values)
    cpu_std = statistics.pstdev(cpu_values) or 1.0
    mem_mean = statistics.mean(mem_values)
    mem_std = statistics.pstdev(mem_values) or 1.0

    cpu_z = (current["cpu_percent"] - cpu_mean) / cpu_std
    mem_z = (current["memory_percent"] - mem_mean) / mem_std

    anomalous = (
        abs(cpu_z) > STD_DEV_THRESHOLD or abs(mem_z) > STD_DEV_THRESHOLD
    )

    return {
        "behavior": "anomalous" if anomalous else "neutral",
        "cpu_z_score": round(cpu_z, 2),
        "memory_z_score": round(mem_z, 2),
        "baseline_samples": len(history),
    }
