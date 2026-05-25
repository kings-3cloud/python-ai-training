### Practice / Machine Problems

# Exercise 1 - C# to Python Translation [K]
Problem statement: Translate this C# logic into idiomatic Python using a dataclass and list comprehension.

var values = new List<int> { 120, 280, 90, 340 };
var labels = values.Select(v => v < 150 ? "healthy" : v < 300 ? "degraded" : "critical");
Expected output:

['healthy', 'degraded', 'healthy', 'critical']
Hint: Use a conditional expression inside a Python list comprehension.


# Exercise 2 - Environment Bootstrap Drill [K]
Problem statement: Create a fresh virtual environment, install requests, and run a script that performs a GET request to https://httpbin.org/get and prints the status code.

Expected output:

200
Hint: Use python -m venv .venv, activate it, and install dependencies with pip before running the script.


# Exercise 3 - Debugging Drill [K]
Problem statement: Given a script that returns critical for average latency 149, find and fix the bug using IDE breakpoints.

Expected output:

healthy
Hint: Inspect conditional boundaries and verify branch ordering.



# Run the app
uv run exercise1.py
uv run exercise2.py
uv run exercise3.py