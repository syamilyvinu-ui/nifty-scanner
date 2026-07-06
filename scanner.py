import yfinance as yf

def get_market_analysis(index):
    # ഇൻഡക്സിന് അനുസരിച്ചുള്ള ticker
    ticker_map = {"NIFTY": "^NSEI", "BANKNIFTY": "^NSEBANK", "FINNIFTY": "^CNXFIN"}
    ticker = ticker_map.get(index, "^NSEI")
    
    # 5 മിനിറ്റ് ഇന്റർവെലിൽ ഡാറ്റ എടുക്കുന്നു
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
    
    # ലോജിക്: CPR + MA Crossing
    if ltp > tc and ma_14 > ma_21:
        return "BUY (STRONG)"
    elif ltp < bc and ma_14 < ma_21:
        return "SELL (STRONG)"
    else:
        return "WAIT/NEUTRAL"
