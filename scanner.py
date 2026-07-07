def get_reversal_signal(df):
    last = df.iloc[-1]
    # Hammer Logic (Body < 1/3 of range, Shadow > 2/3)
    is_hammer = (last['Close'] > last['Open']) and ((last['Close'] - last['Open']) < (last['High'] - last['Low']) / 3)
    
    # Shooting Star Logic
    is_shooting_star = (last['Close'] < last['Open']) and ((last['Open'] - last['Close']) < (last['High'] - last['Low']) / 3)
    
    return is_hammer, is_shooting_star

# സിഗ്നൽ ചെക്കർ ഇങ്ങനെ മാറ്റി എഴുതാം:
def get_final_signal(index):
    # ... (ഡാറ്റ ഡൗൺലോഡ് ചെയ്യുക)
    is_hammer, is_shooting_star = get_reversal_signal(df)
    
    # EMA Crossover + Volume + Candlestick Reversal
    if last['EMA14'] > last['EMA21'] and vol_confirm and is_hammer:
        return last['Close'], "STRONG BUY"
    
    elif last['EMA14'] < last['EMA21'] and vol_confirm and is_shooting_star:
        return last['Close'], "STRONG SELL"
    
    return last['Close'], "HOLD"
