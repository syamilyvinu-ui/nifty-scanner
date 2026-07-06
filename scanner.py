import yfinance as yf

def get_signal(index, ltp):
    # ഇവിടെയാണ് നിങ്ങൾ സപ്പോർട്ട്, റെസിസ്റ്റൻസ്, OI എന്നിവയുടെ ലോജിക് എഴുതേണ്ടത്
    # ഉദാഹരണത്തിന്:
    if ltp > 24000:
        return "BUY (STRONG)"
    elif ltp < 23800:
        return "SELL (STRONG)"
    else:
        return None
