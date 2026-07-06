import streamlit as st
import yfinance as yf
import requests
import time
from scanner import get_cpr_ma_signal

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


# ഇതാണ് മാറ്റേണ്ടത്: last_signal ലൂപ്പിന് പുറത്താക്കുക
if "last_signal" not in st.session_state:
    st.session_state.last_signal = None

if st.button("Start Signal Scanner"):
    st.success(f"Scanning {index} ({timeframe})...")
    while True:
        ltp, signal = get_cpr_ma_signal(index)
        
        # session_state ഉപയോഗിച്ച് സിഗ്നൽ പരിശോധിക്കുന്നു
        if signal != "WAIT/NEUTRAL" and signal != st.session_state.last_signal:
            msg = f"🔔 *SIGNAL DETECTED*\n📈 Index: {index}\n⚡ Action: {signal}\n💰 Price: {ltp}\n🛑 SL: {sl_points}"
            send_telegram(msg)
            st.write(f"Signal Sent: {signal}")
            st.session_state.last_signal = signal 
        
        time.sleep(60)
        st.rerun()
