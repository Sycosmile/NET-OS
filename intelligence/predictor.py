"""Predicts near-term load trend from recently logged metric history."""

from memory.db import fetch_recent_metrics


def predict_load(limit: int = 10) -> dict:
    """Estimate whether CPU load is rising, falling, or stable.

    Uses a simple average-of-first-half vs average-of-second-half
    comparison over the most recent samples — enough to catch a
    real trend without needing a heavier forecasting model.
    """
    rows = fetch_recent_metrics(limit=limit)
    if len(rows) < 4:
        return {
            "prediction": "insufficient_data",
            "samples": len(rows),
        }

    # rows are newest-first; reverse to chronological order
    values = [r["cpu_percent"] for r in reversed(rows)]
    mid = len(values) // 2
    earlier = values[:mid]
    later = values[mid:]
    avg_earlier = sum(earlier) / len(earlier)
    avg_later = sum(later) / len(later)
    delta = avg_later - avg_earlier

    if delta > 5:
        trend = "rising"
    elif delta < -5:
        trend = "falling"
    else:
        trend = "stable"

    return {
        "prediction": trend,
        "avg_earlier": round(avg_earlier, 2),
        "avg_later": round(avg_later, 2),
        "delta": round(delta, 2),
        "samples": len(rows),
    }
