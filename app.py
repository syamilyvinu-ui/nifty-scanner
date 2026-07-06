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

# --- സൈഡ്ബാർ: ബ്രോക്കർ API സെറ്റിംഗ്സ് ---
st.sidebar.header("🔑 Broker API Settings")
broker = st.sidebar.selectbox("Select Broker", ["None", "Zerodha", "Angel One", "Upstox"])
api_key = st.sidebar.text_input("Enter API Key", type="password")
api_secret = st.sidebar.text_input("Enter API Secret", type="password")

# --- മെയിൻ സെറ്റിംഗ്സ് ---
index = st.selectbox("Select Index", ["NIFTY", "BANKNIFTY", "FINNIFTY", "MIDCPNIFTY", "SENSEX"])
timeframe = st.selectbox("Timeframe", ["1m", "5m", "15m"])
sl_points = st.number_input("Stop Loss Points", value=30)

# സിഗ്നൽ ട്രാക്ക് ചെയ്യാൻ session_state ഉപയോഗിക്കുന്നു
if "last_signal" not in st.session_state:
    st.session_state.last_signal = None

if st.button("Start Signal Scanner"):
    st.success(f"Scanning {index} ({timeframe})...")
    
    while True:
        # scanner.py-യിൽ നിന്ന് സിഗ്നൽ എടുക്കുന്നു
        ltp, signal = get_cpr_ma_signal(index)
        
        # ഫിൽട്ടറിംഗ് ലോജിക്
        if signal != "WAIT/NEUTRAL" and signal != st.session_state.last_signal:
            msg = f"🔔 *SIGNAL DETECTED*\n📈 Index: {index}\n⚡ Action: {signal}\n💰 Price: {ltp}\n🛑 SL: {sl_points}"
            send_telegram(msg)
            st.write(f"Signal Sent: {signal}")
            
            # പുതിയ സിഗ്നൽ സേവ് ചെയ്യുന്നു
            st.session_state.last_signal = signal
        
        time.sleep(60) # 1 മിനിറ്റ് ഇടവേള
        st.rerun()
