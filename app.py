import streamlit as st
import requests
import time
import yfinance as yf

# --- CONFIGURATION ---
TOKEN = "8227355571:AAFb7srp8TE5BbQ_o29Bn7tDCcpnYpYPS9I"
CHAT_ID = "945947285"

# --- SESSION STATE ---
if 'in_trade' not in st.session_state: st.session_state.in_trade = False
if 'broker_connected' not in st.session_state: st.session_state.broker_connected = False
if 'h' not in st.session_state: st.session_state.h = 24000.0
if 'l' not in st.session_state: st.session_state.l = 23800.0
if 'c' not in st.session_state: st.session_state.c = 23950.0

# --- FUNCTIONS ---
def get_market_levels(symbol):
    ticker = "^NSEI" if symbol == "NIFTY" else "^NSEBANK"
    data = yf.Ticker(ticker).history(period="2d")
    yesterday = data.iloc[-2]
    return float(yesterday['High']), float(yesterday['Low']), float(yesterday['Close'])

def send_telegram(msg):
    try:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                      json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})
    except: pass

# --- UI ---
st.set_page_config(page_title="ISHA TRADE", layout="wide")
st.title("🚀 ISHA TRADE - Advanced Algo Bot")

# Sidebar - Broker
st.sidebar.header("🔑 Broker Setup")
if st.sidebar.button("Connect Broker"):
    st.session_state.broker_connected = True
    st.sidebar.success("Broker Connected!")

# Power Switch
power_switch = st.toggle("System Power Switch", value=False)

if power_switch:
    st.success("✅ ISHA TRADE System is ON")
    index = st.selectbox("Index", ["NIFTY", "BANKNIFTY"])
    
    # Levels (Auto-Fetch & Flexible)
    if st.button("Fetch Auto Levels"):
        st.session_state.h, st.session_state.l, st.session_state.c = get_market_levels(index)
    
    col1, col2, col3 = st.columns(3)
    with col1: st.session_state.h = st.number_input("High", value=st.session_state.h)
    with col2: st.session_state.l = st.number_input("Low", value=st.session_state.l)
    with col3: st.session_state.c = st.number_input("Close", value=st.session_state.c)
    
    sl_points = st.number_input("Stop Loss Points", value=30)
        
    pivot = (st.session_state.h + st.session_state.l + st.session_state.c) / 3
    tc = (pivot - (st.session_state.h + st.session_state.l) / 2) + pivot
    bc = (st.session_state.h + st.session_state.l) / 2

    if st.button("Start ISHA BOT"):
        while power_switch:
            # ലൈവ് ഡാറ്റ (API ഡാറ്റ ഇവിടെ വരുക)
            ltp, pcr, oi = 23980.0, 1.2, 50000 
            
            if not st.session_state.in_trade:
                if ltp > tc and pcr > 1.1 and oi > 0:
                    st.session_state.in_trade = True
                    st.session_state.entry_price = ltp
                    send_telegram(f"🔔 *ISHA TRADE ENTRY*\nSide: BUY\nPrice: {ltp}\nSL: {ltp - sl_points}")
            else:
                if ltp < tc or ltp <= (st.session_state.entry_price - sl_points):
                    st.session_state.in_trade = False
                    send_telegram("✅ *ISHA TRADE EXIT*")
            
            time.sleep(30)
else:
    st.warning("⚠️ ISHA TRADE System is OFF")
