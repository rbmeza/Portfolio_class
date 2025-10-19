import requests
import os

class Stock:
    def __init__(self, symbol: str, shares: float):
        self.symbol = symbol
        self.shares = shares
        self.current_price = self.get_current_price()
    
    def get_current_price(self) -> float:
        """Get current price of the stock from the API."""

        try:
            response = requests.get(f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={self.symbol}&outputsize=compact&apikey={os.getenv('API_KEY')}").json()
            last_refreshed = response["Meta Data"]["3. Last Refreshed"]
            price = response["Time Series (Daily)"][last_refreshed]["4. close"]
        except Exception:
            print(f"Error obtaining price for {self.symbol}")
            return 100

        return float(price)

    @property
    def value(self) -> float:
        """Return the value of the stock (price * shares)."""
        return self.shares * self.current_price


class Portfolio:
    def __init__(self, stocks: list[Stock], target_allocation: dict[str, float]):
        """
        stocks: Stocks objects
        target_allocation: Needed distribution, for example: {'META': 0.4, 'AAPL': 0.6}
        """
        self.stocks = {s.symbol: s for s in stocks}

        if sum(target_allocation.values()) != 1:
            raise ValueError("Sum of the distributions must be 1")
        self.target_allocation = target_allocation

    def total_value(self) -> float:
        """Return the total value of the portfolio."""
        return sum(stock.value for stock in self.stocks.values())

    def rebalance(self) -> dict[str, dict[str, float]]:
        """
        Calculate how much to buy or sell of each stock to reach the target.
        Returns a dictionary with the difference per stock.
        """
        total_value = self.total_value()
        adjustments = {}

        for stock in self.stocks.values():

            # Assume that if the stock is not in the target allocation, the target is 0
            target_pct = self.target_allocation.get(stock.symbol)
            if target_pct is None:
                target_pct = 0
            
            current_value = stock.value
            target_value = total_value * target_pct
            diff_value = target_value - current_value
            diff_shares = diff_value / stock.current_price
            adjustments[stock.symbol] = {
                "current_value": current_value,
                "target_value": target_value,
                "diff_value": diff_value,
                "diff_shares": diff_shares,
                "action": "BUY" if diff_value > 0 else "SELL" if diff_value < 0 else "HOLD"
            }

        return adjustments


# ===== Usage =====
if __name__ == "__main__":
    nvidia = Stock("NVDA", shares=50)
    aapl = Stock("AAPL", shares=20)
    meta = Stock("META", shares=10)
    tsla = Stock("TSLA", shares=15)

    portfolio = Portfolio(
        stocks=[nvidia, aapl, meta, tsla],
        target_allocation={"NVDA": 0.3, "AAPL": 0.4, "META": 0.3}
    )

    rebalance_plan = portfolio.rebalance()
    print(f"Total value: ${portfolio.total_value():.2f}")
    print("--------------------------------")

    for symbol, info in rebalance_plan.items():
        print(f"{symbol}: {info['action']} {abs(info['diff_shares']):.2f} shares "
              f"(${abs(info['diff_value']):.2f})")

        print(f"Target allocation: {info['target_value']:.2f}")
        print("--------------------------------")

