import yfinance as yf

def get_cpr_ma_signal(index):
    ticker_map = {"NIFTY": "^NSEI", "BANKNIFTY": "^NSEBANK", "FINNIFTY": "^CNXFIN"}
    ticker = ticker_map.get(index, "^NSEI")
    
    # Volume കൂടി ഉൾപ്പെടുത്തി ഡാറ്റ എടുക്കുന്നു
    data = yf.Ticker(ticker).history(period="5d", interval="5m")
    
    # CPR & MA കണക്കുകൂട്ടൽ
    high = data['High'].iloc[-2]
    low = data['Low'].iloc[-2]
    close = data['Close'].iloc[-2]
    pivot = (high + low + close) / 3
    bc = (high + low) / 2
    tc = (pivot - bc) + pivot
    
    ma_14 = data['Close'].rolling(window=14).mean().iloc[-1]
    ma_21 = data['Close'].rolling(window=21).mean().iloc[-1]
    
    # വോളിയം ചെക്കിംഗ് (കഴിഞ്ഞ 10 കാൻഡിലുകളുടെ ശരാശരി വോളിയത്തേക്കാൾ കൂടുതലാണോ?)
    avg_volume = data['Volume'].rolling(window=10).mean().iloc[-1]
    current_volume = data['Volume'].iloc[-1]
    
    ltp = float(data['Close'].iloc[-1])
    
    # വോളിയം സ്പൈക്ക് ഉണ്ടോ എന്ന് നോക്കുന്നു
    volume_ok = current_volume > avg_volume

    if ltp > tc and ma_14 > ma_21 and volume_ok:
        return ltp, "BUY (STRONG + VOLUME)"
    elif ltp < bc and ma_14 < ma_21 and volume_ok:
        return ltp, "SELL (STRONG + VOLUME)"
    else:
        return ltp, "WAIT/NEUTRAL"
