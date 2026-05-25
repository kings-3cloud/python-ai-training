# Buggy version (wrong condition order — 149 returns "critical"):
# def classify(v):
#     if v >= 300:
#         return "critical"
#     elif v >= 150:   # bug: this catches everything below 300, including 149
#         return "degraded"
#     else:
#         return "healthy"

# Fixed version (ascending boundary checks):
def classify(v: float) -> str:
    if v < 150:
        return "healthy"
    elif v < 300:
        return "degraded"
    else:
        return "critical"


average_latency = 149
print(classify(average_latency))  # healthy
