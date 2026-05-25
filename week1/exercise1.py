from dataclasses import dataclass


@dataclass
class LatencyResult:
    value: int
    label: str


values = [120, 280, 90, 340]

results = [
    LatencyResult(v, "healthy" if v < 150 else "degraded" if v < 300 else "critical")
    for v in values
]

labels = [r.label for r in results]
print(labels)
