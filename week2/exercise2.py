class Invoice:
    def __init__(self, client: str, lines: list[float]) -> None:
        self.client = client
        self.lines = lines

    def total(self, tax: float) -> float:
        return sum(self.lines) * (1 + tax)

    def __str__(self) -> str:
        return f"Invoice<{self.client}>: total={self.total(0.12):.2f}"


invoice = Invoice("Acme", [50.0, 30.0, 10.0])
print(invoice)
