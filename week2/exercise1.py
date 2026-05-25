services = [
    {"name": "orders",  "status_code": 200, "latency_ms": 120},
    {"name": "billing", "status_code": 200, "latency_ms": 450},
    {"name": "search",  "status_code": 503, "latency_ms": 820},
]


def classify(status_code: int, latency_ms: int) -> str:
    if status_code >= 500:
        return "critical"
    elif latency_ms > 300:
        return "degraded"
    else:
        return "healthy"


def summarize(responses: list[dict]) -> tuple[dict[str, str], list[str]]:
    health = {s["name"]: classify(s["status_code"], s["latency_ms"]) for s in responses}
    slow   = [s["name"] for s in responses if s["latency_ms"] > 300]
    return health, slow


print(summarize(services))
