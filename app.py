import streamlit as st
import yfinance as yf
import requests
import time
from scanner import get_cpr_ma_signal

TOKEN = "8227355571:AAFb7srp8TE5BbQ_o29Bn7tDCcpnYpYPS9I"
CHAT_ID = "945947285"

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})

st.set_page_config(page_title="ISHA ALGO BOT", layout="wide")
st.title("🚀 ISHA SMART ALGO SCANNER (PRO)")

# Session State Setup
if "active_trade" not in st.session_state:
    st.session_state.active_trade = None # {'side': 'BUY', 'entry': 100}

# Settings
index = st.selectbox("Select Index", ["NIFTY", "BANKNIFTY"])
sl_points = st.number_input("Stop Loss Points", value=20)
target_points = st.number_input("Target Points", value=40)

if st.button("Start Signal Scanner"):
    while True:
          ltp, signal = get_ma_crossover_signal(index) # <-- പുതിയത്

        
        # 1. നിലവിൽ ട്രേഡ് ഇല്ലെങ്കിൽ പുതിയ എൻട്രി നോക്കുന്നു
        if st.session_state.active_trade is None:
            if signal in ["BUY", "SELL"]:
                st.session_state.active_trade = {'side': signal, 'entry': ltp}
                send_telegram(f"🎯 *NEW ENTRY*\nSide: {signal}\nPrice: {ltp}")
        
        # 2. ട്രേഡ് ഉണ്ടെങ്കിൽ എക്സിറ്റ് കണ്ടീഷൻ ചെക്ക് ചെയ്യുന്നു
        else:
            trade = st.session_state.active_trade
            exit_msg = None
            
            if trade['side'] == "BUY":
                if ltp <= (trade['entry'] - sl_points): exit_msg = "🛑 SL HIT (BUY)"
                elif ltp >= (trade['entry'] + target_points): exit_msg = "✅ TARGET HIT (BUY)"
            
            elif trade['side'] == "SELL":
                if ltp >= (trade['entry'] + sl_points): exit_msg = "🛑 SL HIT (SELL)"
                elif ltp <= (trade['entry'] - target_points): exit_msg = "✅ TARGET HIT (SELL)"
            
            if exit_msg:
                send_telegram(f"{exit_msg}\nExit Price: {ltp}")
                st.session_state.active_trade = None # ട്രേഡ് ക്ലോസ് ചെയ്തു
        
        time.sleep(60)
        st.rerun()
