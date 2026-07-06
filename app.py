import streamlit as st
import yfinance as yf
import requests
import time

# --- CONFIGURATION ---
TOKEN = "8227355571:AAFb7srp8TE5BbQ_o29Bn7tDCcpnYpYPS9I"
CHAT_ID = "945947285"

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})

st.set_page_config(page_title="ISHA ALGO BOT", layout="wide")
st.title("🚀 ISHA SMART ALGO SCANNER")

# User Inputs
index = st.selectbox("Select Index", ["NIFTY", "BANKNIFTY", "FINNIFTY", "MIDCPNIFTY", "SENSEX"])
timeframe = st.selectbox("Timeframe", ["1m", "5m", "15m"])
sl_points = st.number_input("Stop Loss Points", value=30)

if st.button("Start Signal Scanner"):
    st.success(f"Scanning {index} ({timeframe})...")
    while True:
        # 1. ലൈവ് പ്രൈസ് എടുക്കുന്നു
        ticker = {"NIFTY": "^NSEI", "BANKNIFTY": "^NSEBANK", "FINNIFTY": "^CNXFIN"}.get(index, "^NSEI")
        ltp = float(yf.Ticker(ticker).history(period="1d", interval="1m")['Close'].iloc[-1])
        
        # 2. Logic (CPR + OI + Volume) - ഇവിടെ ഡാറ്റ വിശകലനം ചെയ്യുന്നു
        # ഉദാഹരണ ലോജിക്: വോളിയം സ്പൈക്കും പ്രൈസ് മൂവ്മെന്റും നോക്കുന്നു
        from scanner import get_market_analysis # scanner-ൽ നിന്ന് ലോജിക് എടുക്കുന്നു

# ... loop-ന്റെ ഉള്ളിൽ ...
signal = get_market_analysis(index) 

if signal != "WAIT/NEUTRAL": 
    # ടെലിഗ്രാം അലേർട്ട് അയക്കുന്നു
    msg = f"🔔 *SIGNAL DETECTED*\n📈 Index: {index}\n⚡ Action: {signal}\n💰 Price: {ltp}"
    send_telegram(msg)
            # ടെലിഗ്രാം അലേർട്ട്
            msg = f"🔔 *SIGNAL DETECTED*\n📈 Index: {index}\n⚡ Action: {signal}\n💰 Price: {ltp}\n🛑 SL: {sl_points}"
            send_telegram(msg)
            st.write(f"Signal Sent: {signal}")
        
        time.sleep(60) # 1 മിനിറ്റ് ഇടവേള
        st.rerun()
