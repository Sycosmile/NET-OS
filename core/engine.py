"""The core engine: one orchestrated tick of the Net-OS control loop."""

from intelligence.health import system_health, collect_metrics
from intelligence.predictor import predict_load
from intelligence.behavior import analyze_behavior
from intelligence.strategy import get_strategy
from memory.db import log_metrics, log_event


def run_engine() -> dict:
    """Run one full engine tick: collect, store, analyze, decide.

    This is the real control loop step — it samples live system
    metrics, persists them, then runs prediction, anomaly detection,
    and strategy selection on top of that history. Each of those
    intelligence functions reads from the same persisted history,
    so this is what actually wires the modules together.
    """
    raw = collect_metrics()
    log_metrics(
        raw["cpu_percent"],
        raw["memory_percent"],
        raw["net_sent"],
        raw["net_recv"],
    )

    health = system_health()
    prediction = predict_load()
    behavior = analyze_behavior()
    strategy = get_strategy()

    if behavior.get("behavior") == "anomalous":
        log_event(
            "anomaly_detected",
            f"cpu_z={behavior['cpu_z_score']} mem_z={behavior['memory_z_score']}",
        )

    log_event(
        "engine_tick",
        f"health={health['overall']} strategy={strategy['strategy']}",
    )

    return {
        "engine": "active",
        "status": "running",
        "health": health,
        "prediction": prediction,
        "behavior": behavior,
        "strategy": strategy,
    }
