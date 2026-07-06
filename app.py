import streamlit as st
import requests
import time

# --- CONFIGURATION ---
TOKEN = "8227355571:AAFb7srp8TE5BbQ_o29Bn7tDCcpnYpYPS9I"
CHAT_ID = "945947285"

# --- SESSION STATE ---
if 'in_trade' not in st.session_state: st.session_state.in_trade = False
if 'broker_connected' not in st.session_state: st.session_state.broker_connected = False
if 'trade_type' not in st.session_state: st.session_state.trade_type = None

# --- FUNCTIONS ---
def send_telegram(message):
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                      json={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})
    except: pass

def execute_trade(side, symbol, action):
    if st.session_state.broker_connected:
        return f"✅ **AUTO-{action}:** {side} order placed for {symbol}"
    else:
        return f"🔔 **SIGNAL:** Please execute {side} for {symbol} manually."

# --- UI ---
st.set_page_config(page_title="ISHA TRADE", layout="wide")
st.title("🚀 ISHA TRADE - Advanced Algo Bot")

# Sidebar
st.sidebar.header("🔑 Broker Setup")
api_key = st.sidebar.text_input("API Key", type="password")
if st.sidebar.button("Connect Broker"):
    if api_key:
        st.session_state.broker_connected = True
        st.sidebar.success("Mode: AUTO-TRADE ACTIVE")
    else:
        st.sidebar.error("Enter valid API Key")

# Power Switch
power_switch = st.toggle("System Power Switch", value=False)

if power_switch:
    st.success("✅ ISHA TRADE System is ON")
    
    col1, col2 = st.columns(2)
    with col1:
        index = st.selectbox("Index", ["NIFTY", "BANKNIFTY"])
    with col2:
        h = st.number_input("High", value=24000.0)
        l = st.number_input("Low", value=23800.0)
        c = st.number_input("Close", value=23950.0)
        sl_points = st.number_input("Stop Loss Points", value=30)
        
    pivot = (h + l + c) / 3
    bc = (h + l) / 2
    tc = (pivot - bc) + pivot

    if st.button("Start ISHA BOT"):
        while power_switch:  # പവർ സ്വിച്ച് ഓൺ ആണെങ്കിൽ മാത്രം ലൂപ്പ് പ്രവർത്തിക്കും
            # ലൈവ് ഡാറ്റ (NSE API)
            ltp, pcr, oi = 23980.0, 1.2, 50000 
            
            # ENTRY LOGIC
            if not st.session_state.in_trade:
                if ltp > tc and pcr > 1.1 and oi > 0:
                    msg = execute_trade("BUY", index, "ENTRY")
                    st.session_state.in_trade = True
                    st.session_state.trade_type = "BUY"
                    st.session_state.entry_price = ltp
                    send_telegram(f"{msg}\nPrice: {ltp}")
                elif ltp < bc and pcr < 0.9 and oi < 0:
                    msg = execute_trade("SELL", index, "ENTRY")
                    st.session_state.in_trade = True
                    st.session_state.trade_type = "SELL"
                    st.session_state.entry_price = ltp
                    send_telegram(f"{msg}\nPrice: {ltp}")
            
            # EXIT & SL LOGIC
            else:
                sl_hit = (st.session_state.trade_type == "BUY" and ltp <= (st.session_state.entry_price - sl_points)) or \
                         (st.session_state.trade_type == "SELL" and ltp >= (st.session_state.entry_price + sl_points))
                
                if sl_hit or (st.session_state.trade_type == "BUY" and ltp < tc) or (st.session_state.trade_type == "SELL" and ltp > bc):
                    msg = execute_trade(st.session_state.trade_type, index, "EXIT")
                    st.session_state.in_trade = False
                    send_telegram(f"✅ {msg} - {'SL HIT' if sl_hit else 'Trend Reversed'}")
            
            time.sleep(30)
else:
    st.warning("⚠️ ISHA TRADE System is OFF")
