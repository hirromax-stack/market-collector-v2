from flask import Flask
import json
import yfinance as yf
import pandas as pd
import traceback
from datetime import datetime, timezone
from pathlib import Path

app = Flask(__name__)
CONFIG_FILE = "config.json"

def load_config():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

@app.route('/')
def run_collector():
    try:
        config = load_config()
        symbols = []
        for group in config["symbols"].values():
            symbols.extend(group)
        
        # Logique simplifiée pour l'exemple
        data = []
        for symbol in symbols[:3]:  # Limité pour la démo
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="1d")
            if not hist.empty:
                data.append({
                    "symbol": symbol,
                    "price": round(hist["Close"].iloc[-1], 2)
                })
        
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(5000))