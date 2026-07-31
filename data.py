import requests

from config import API_KEY, PAIRS, INTERVAL, CANDLES

from analysis import (
    get_trend,
    detect_bos,
    detect_choch,
    detect_fvg,
    detect_order_block,
    detect_liquidity_sweep,
    get_signal,
    get_confidence,
    predict_next_candle,
)

URL = "https://api.twelvedata.com/time_series"


def get_market_data():

    market = []

    for pair in PAIRS:

        params = {
            "symbol": pair,
            "interval": INTERVAL,
            "outputsize": CANDLES,
            "apikey": API_KEY
        }

        try:

            response = requests.get(
                URL,
                params=params,
                timeout=10
            )

            data = response.json()

            if "values" not in data:
                continue

            candles = data["values"]
            latest = candles[0]

            market.append({

                "pair": pair,
                "trend": get_trend(candles),
                "bos": detect_bos(candles),
                "choch": detect_choch(candles),
                "fvg": detect_fvg(candles),
                "order_block": detect_order_block(candles),
                "liquidity": detect_liquidity_sweep(candles),
                "signal": get_signal(candles),
                "confidence": get_confidence(candles),
                "prediction": predict_next_candle(candles),

                "open": latest["open"],
                "high": latest["high"],
                "low": latest["low"],
                "close": latest["close"]

            })

        except Exception as e:
            print(pair, e)

    return market