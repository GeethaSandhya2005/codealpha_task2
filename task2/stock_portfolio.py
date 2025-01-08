import requests

class StockPortfolio:
    def __init__(self):
        self.portfolio = {}

    def add_stock(self, symbol, shares, purchase_price):
        """Add or update stock information in the portfolio."""
        if symbol in self.portfolio:
            self.portfolio[symbol]['shares'] += shares
        else:
            self.portfolio[symbol] = {
                'shares': shares,
                'purchase_price': purchase_price
            }
        print(f"\nAdded {shares} shares of {symbol} at ${purchase_price:.2f} per share.")

    def remove_stock(self, symbol):
        """Remove a stock from the portfolio."""
        if symbol in self.portfolio:
            del self.portfolio[symbol]
            print(f"\nRemoved {symbol} from your portfolio.")
        else:
            print(f"\nStock {symbol} not found in your portfolio.")

    def get_stock_data(self, symbol):
        """Fetch real-time stock price from the Alpha Vantage API."""
        api_key = "your_api_key_here"  # Replace with your Alpha Vantage API key
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if "Global Quote" in data and "05. price" in data["Global Quote"]:
                return float(data["Global Quote"]["05. price"])
            else:
                print(f"\nNo data found for {symbol}.")
                return None
        except requests.exceptions.RequestException as e:
            print(f"\nError fetching stock data for {symbol}: {e}")
            return None

    def display_portfolio(self):
        """Display the portfolio with current stock performance."""
        print("\nYour Portfolio:")
        total_value = 0
        for symbol, details in self.portfolio.items():
            current_price = self.get_stock_data(symbol)
            if current_price is not None:
                stock_value = current_price * details['shares']
                total_value += stock_value
                print(f"{symbol}: {details['shares']} shares | "
                      f"Purchase Price: ${details['purchase_price']:.2f} | "
                      f"Current Price: ${current_price:.2f} | "
                      f"Total Value: ${stock_value:.2f}")
            else:
                print(f"{symbol}: {details['shares']} shares | "
                      f"Purchase Price: ${details['purchase_price']:.2f} | "
                      f"Current Price: N/A")
        print(f"\nTotal Portfolio Value: ${total_value:.2f}")

def main():
    """Main function to interact with the stock portfolio tracker."""
    portfolio = StockPortfolio()

    while True:
        print("\nStock Portfolio Tracker")
        print("1. Add Stock")
        print("2. Remove Stock")
        print("3. View Portfolio")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            symbol = input("Enter stock symbol (e.g., AAPL, TSLA): ").upper()
            try:
                shares = int(input("Enter the number of shares: "))
                purchase_price = float(input("Enter the purchase price per share: "))
                portfolio.add_stock(symbol, shares, purchase_price)
            except ValueError:
                print("\nInvalid input. Please enter numeric values for shares and price.")

        elif choice == "2":
            symbol = input("Enter stock symbol to remove: ").upper()
            portfolio.remove_stock(symbol)

        elif choice == "3":
            portfolio.display_portfolio()

        elif choice == "4":
            print("\nExiting Stock Portfolio Tracker. Goodbye!")
            break

        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main()




