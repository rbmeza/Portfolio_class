class Stock:
    def __init__(self, symbol: str, shares: float, current_price: float):
        self.symbol = symbol
        self.shares = shares
        self.current_price = current_price

    @property
    def value(self) -> float:
        """Devuelve el valor total de esta acción (precio * cantidad)."""
        return self.shares * self.current_price


class Portfolio:
    def __init__(self, stocks: list[Stock], target_allocation: dict[str, float]):
        """
        stocks: lista de objetos Stock actuales en el portafolio
        target_allocation: distribución deseada en porcentaje (suma = 1)
                           ejemplo: {'META': 0.4, 'AAPL': 0.6}
        """
        self.stocks = {s.symbol: s for s in stocks}
        self.target_allocation = target_allocation

    def total_value(self) -> float:
        """Devuelve el valor total actual del portafolio."""
        return sum(stock.value for stock in self.stocks.values())

    def rebalance(self) -> dict[str, dict[str, float]]:
        """
        Calcula cuánto comprar o vender de cada acción para alcanzar el target.
        Retorna un diccionario con la diferencia por acción.
        """
        total_value = self.total_value()
        adjustments = {}

        for symbol, target_pct in self.target_allocation.items():
            stock = self.stocks.get(symbol)
            current_value = stock.value if stock else 0
            target_value = total_value * target_pct
            diff_value = target_value - current_value
            diff_shares = diff_value / stock.current_price if stock else target_value / 1  # suponemos precio=1 si no hay stock

            adjustments[symbol] = {
                "current_value": current_value,
                "target_value": target_value,
                "diff_value": diff_value,
                "diff_shares": diff_shares,
                "action": "BUY" if diff_value > 0 else "SELL" if diff_value < 0 else "HOLD"
            }

        return adjustments


# ===== Ejemplo de uso =====
if __name__ == "__main__":
    meta = Stock("META", shares=30, current_price=400)
    aapl = Stock("AAPL", shares=10, current_price=200)

    portfolio = Portfolio(
        stocks=[meta, aapl],
        target_allocation={"META": 0.4, "AAPL": 0.6}
    )

    rebalance_plan = portfolio.rebalance()

    for symbol, info in rebalance_plan.items():
        print(f"{symbol}: {info['action']} {abs(info['diff_shares']):.2f} shares "
              f"(${abs(info['diff_value']):.2f})")
