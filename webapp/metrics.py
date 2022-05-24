import prometheus_client
from prometheus_client import multiprocess as prom_mp


def register() -> prometheus_client.CollectorRegistry:
    registry = prometheus_client.CollectorRegistry()
    prom_mp.MultiProcessCollector(registry)
    return registry
