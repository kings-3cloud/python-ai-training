### Practice / Machine Problems

# Exercise 1 — Service Health Summarizer [K] (10 minutes)
Problem statement: Given a list of service responses (name, status_code, latency_ms), write a function that returns:

a dictionary of service_name -> "healthy" | "degraded" | "critical", and
a list of services with latency greater than 300ms.
Expected output (shape):

(
    {"orders": "healthy", "billing": "degraded", "search": "critical"},
    ["billing", "search"]
)
Hint: Use one if/elif/else function for status classification, then use list/dict comprehensions for output.

# Exercise 2 — Rewrite from C# to Python [K] (10–12 minutes)
Problem statement: Translate this C# logic into idiomatic Python using a class, constructor, and a computed summary method.

public class Invoice {
    public string Client { get; set; }
    public List<decimal> Lines { get; set; } = new();

    public decimal Total(decimal tax) {
        return Lines.Sum() * (1 + tax);
    }
}
Python requirements:

Use __init__, type hints, and a total() method.
Add a readable __str__ representation.
Demonstrate one call with tax = 0.12.
Expected output (shape): Invoice<Acme>: total=123.20

Hint: Model Lines as list[float], and use sum(self.lines) in total().


# Run the app
uv run exercise1.py
uv run exercise2.py