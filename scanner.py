import yfinance as yf

# ഫങ്ഷൻ പേര് ഇതാക്കി മാറ്റുക:
def get_cpr_ma_signal(index): 
    ticker_map = {"NIFTY": "^NSEI", "BANKNIFTY": "^NSEBANK", "FINNIFTY": "^CNXFIN"}
    ticker = ticker_map.get(index, "^NSEI")
    
    data = yf.Ticker(ticker).history(period="5d", interval="5m")
    
    # CPR കണക്കുകൂട്ടൽ
    high = data['High'].iloc[-2]
    low = data['Low'].iloc[-2]
    close = data['Close'].iloc[-2]
    pivot = (high + low + close) / 3
    bc = (high + low) / 2
    tc = (pivot - bc) + pivot
    
    # MA 14 & 21 കണക്കുകൂട്ടൽ
    ma_14 = data['Close'].rolling(window=14).mean().iloc[-1]
    ma_21 = data['Close'].rolling(window=21).mean().iloc[-1]
    
    # ലൈവ് പ്രൈസ്
    ltp = float(data['Close'].iloc[-1])
    
    # ലോജിക്
    if ltp > tc and ma_14 > ma_21:
        return ltp, "BUY (STRONG)" # ഇവിടെ ltp കൂടി റിട്ടേൺ ചെയ്യണം
    elif ltp < bc and ma_14 < ma_21:
        return ltp, "SELL (STRONG)"
    else:
        return ltp, "WAIT/NEUTRAL"
