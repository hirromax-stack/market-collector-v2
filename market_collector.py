import json
import yfinance as yf
from datetime import datetime

CONFIG_FILE = "config.json"

def load_config():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def fetch_prices(symbols):
    data = {}
    for symbol in symbols:
        ticker = yf.Ticker(symbol)
        price = ticker.history(period="1d")["Close"]
        if not price.empty:
            data[symbol] = round(price.iloc[-1], 4)
    return data

def main():
print("=" * 60)
print("📊 Market Collector started")
print("=" * 60)

    config = load_config()
    all_symbols = []

    for category in config["symbols"].values():
        all_symbols.extend(category)

    prices = fetch_prices(all_symbols)

    print(f"\n📊 Market Snapshot — {datetime.utcnow()} UTC\n")
    for symbol, price in prices.items():
        print(f"{symbol:<10} {price}")
print("=" * 60)
print("✅ Market Collector finished successfully")
print("=" * 60)

if __name__ == "__main__":
    main()
