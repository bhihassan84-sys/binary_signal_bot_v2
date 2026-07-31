def get_trend(candles):

    if len(candles) < 20:
        return "⚪ NO DATA"

    candles = list(reversed(candles))

    first_close = float(candles[0]["close"])
    last_close = float(candles[-1]["close"])

    if last_close > first_close:
        return "🟢 UPTREND"

    elif last_close < first_close:
        return "🔴 DOWNTREND"

    return "⚪ SIDEWAYS"



def detect_bos(candles):

    if len(candles) < 2:
        return "No BOS"

    latest = candles[0]
    previous = candles[1]

    if float(latest["high"]) > float(previous["high"]):
        return "🟢 Bullish BOS"

    elif float(latest["low"]) < float(previous["low"]):
        return "🔴 Bearish BOS"

    return "No BOS"



def detect_choch(candles):

    if len(candles) < 3:
        return "No CHoCH"


    latest = candles[0]
    previous = candles[1]
    third = candles[2]


    if (
        float(previous["high"]) > float(third["high"])
        and float(latest["low"]) < float(previous["low"])
    ):
        return "🔴 Bearish CHoCH"


    elif (
        float(previous["low"]) < float(third["low"])
        and float(latest["high"]) > float(previous["high"])
    ):
        return "🟢 Bullish CHoCH"


    return "No CHoCH"



def detect_fvg(candles):

    if len(candles) < 3:
        return "No FVG"


    candle1 = candles[2]
    candle3 = candles[0]


    high1 = float(candle1["high"])
    low1 = float(candle1["low"])

    high3 = float(candle3["high"])
    low3 = float(candle3["low"])


    if low3 > high1:
        return "🟢 Bullish FVG"


    elif high3 < low1:
        return "🔴 Bearish FVG"


    return "No FVG"



def candle_momentum(candles):

    latest = candles[0]

    open_price = float(latest["open"])
    close_price = float(latest["close"])


    if close_price > open_price:
        return "🟢 Bullish Candle"

    elif close_price < open_price:
        return "🔴 Bearish Candle"

    return "⚪ Neutral Candle"



def candle_strength(candles):

    latest = candles[0]

    high = float(latest["high"])
    low = float(latest["low"])

    open_price = float(latest["open"])
    close_price = float(latest["close"])


    total_range = high - low


    if total_range == 0:
        return 0


    body = abs(close_price - open_price)

    return round((body / total_range) * 100,2)



def detect_order_block(candles):

    if len(candles) < 3:
        return "No OB"


    previous = candles[1]
    latest = candles[0]


    previous_open = float(previous["open"])
    previous_close = float(previous["close"])

    latest_open = float(latest["open"])
    latest_close = float(latest["close"])



    if previous_close < previous_open and latest_close > latest_open:
        return "🟢 Bullish OB"


    elif previous_close > previous_open and latest_close < latest_open:
        return "🔴 Bearish OB"


    return "No OB"




def detect_liquidity_sweep(candles):

    if len(candles) < 2:
        return "No Sweep"


    latest = candles[0]
    previous = candles[1]


    high = float(latest["high"])
    low = float(latest["low"])

    previous_high = float(previous["high"])
    previous_low = float(previous["low"])

    close = float(latest["close"])



    if high > previous_high and close < previous_high:
        return "🔴 High Sweep"


    elif low < previous_low and close > previous_low:
        return "🟢 Low Sweep"


    return "No Sweep"




def get_signal(candles):

    trend = get_trend(candles)
    bos = detect_bos(candles)
    choch = detect_choch(candles)
    fvg = detect_fvg(candles)
    ob = detect_order_block(candles)
    sweep = detect_liquidity_sweep(candles)

    momentum = candle_momentum(candles)
    strength = candle_strength(candles)



    # Weak candle filter

    if strength < 55:
        return "⚪ WAIT"



    # Conflict filter

    if (
        trend == "🟢 UPTREND"
        and bos == "🔴 Bearish BOS"
    ):
        return "⚪ WAIT"


    if (
        trend == "🔴 DOWNTREND"
        and bos == "🟢 Bullish BOS"
    ):
        return "⚪ WAIT"




    # CALL setup

    call_confirmation = 0


    if trend == "🟢 UPTREND":
        call_confirmation += 1


    if bos == "🟢 Bullish BOS":
        call_confirmation += 1


    if momentum == "🟢 Bullish Candle":
        call_confirmation += 1


    if (
        ob == "🟢 Bullish OB"
        or fvg == "🟢 Bullish FVG"
        or sweep == "🟢 Low Sweep"
    ):
        call_confirmation += 1



    # PUT setup

    put_confirmation = 0


    if trend == "🔴 DOWNTREND":
        put_confirmation += 1


    if bos == "🔴 Bearish BOS":
        put_confirmation += 1


    if momentum == "🔴 Bearish Candle":
        put_confirmation += 1


    if (
        ob == "🔴 Bearish OB"
        or fvg == "🔴 Bearish FVG"
        or sweep == "🔴 High Sweep"
    ):
        put_confirmation += 1




    if call_confirmation >= 3:
        return "🟢 CALL"



    if put_confirmation >= 3:
        return "🔴 PUT"



    return "⚪ WAIT"




def get_confidence(candles):

    trend = get_trend(candles)
    bos = detect_bos(candles)
    choch = detect_choch(candles)
    fvg = detect_fvg(candles)
    ob = detect_order_block(candles)
    sweep = detect_liquidity_sweep(candles)

    signal = get_signal(candles)
    strength = candle_strength(candles)


    confidence = 50


    # WAIT filter
    if signal == "⚪ WAIT":
        confidence = 50

        if trend not in ["⚪ SIDEWAYS", "⚪ NO DATA"]:
            confidence += 5

        if bos != "No BOS":
            confidence += 5

        if strength >= 60:
            confidence += 5


        # WAIT maximum 65%
        if confidence > 65:
            confidence = 65


        return f"{confidence}%"



    # Trend confirmation
    if trend not in ["⚪ SIDEWAYS", "⚪ NO DATA"]:
        confidence += 10



    # BOS confirmation
    if bos != "No BOS":
        confidence += 10



    # CHoCH confirmation
    if choch != "No CHoCH":
        confidence += 5



    # Smart Money confirmation

    if ob != "No OB":
        confidence += 5


    if fvg != "No FVG":
        confidence += 5


    if sweep != "No Sweep":
        confidence += 5



    # Candle strength

    if strength >= 80:
        confidence += 15

    elif strength >= 60:
        confidence += 10



    # Final signal boost

    if signal in ["🟢 CALL", "🔴 PUT"]:
        confidence += 10



    if confidence > 95:
        confidence = 95


    if confidence < 50:
        confidence = 50


    return f"{confidence}%"




def predict_next_candle(candles):

    signal = get_signal(candles)


    if signal == "🟢 CALL":
        return "🟢 NEXT CANDLE CALL"


    elif signal == "🔴 PUT":
        return "🔴 NEXT CANDLE PUT"


    return "⚪ WAIT"