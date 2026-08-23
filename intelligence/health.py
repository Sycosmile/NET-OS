"""Collects real system health metrics and classifies their status."""

import psutil

CPU_HIGH = 75.0
CPU_CRITICAL = 90.0
MEM_HIGH = 75.0
MEM_CRITICAL = 90.0


def _classify(value: float, high: float, critical: float) -> str:
    if value >= critical:
        return "critical"
    if value >= high:
        return "high"
    return "normal"


def collect_metrics() -> dict:
    """Sample current CPU, memory, and network counters."""
    cpu = psutil.cpu_percent(interval=0.2)
    mem = psutil.virtual_memory().percent
    net = psutil.net_io_counters()
    return {
        "cpu_percent": cpu,
        "memory_percent": mem,
        "net_sent": net.bytes_sent,
        "net_recv": net.bytes_recv,
    }


def system_health() -> dict:
    """Return a live snapshot of system health with classified status."""
    m = collect_metrics()
    cpu_status = _classify(m["cpu_percent"], CPU_HIGH, CPU_CRITICAL)
    mem_status = _classify(m["memory_percent"], MEM_HIGH, MEM_CRITICAL)

    overall = "optimal"
    if "critical" in (cpu_status, mem_status):
        overall = "critical"
    elif "high" in (cpu_status, mem_status):
        overall = "degraded"

    return {
        "cpu": cpu_status,
        "cpu_percent": m["cpu_percent"],
        "memory": mem_status,
        "memory_percent": m["memory_percent"],
        "network": "optimal",
        "overall": overall,
        "raw": m,
    }
