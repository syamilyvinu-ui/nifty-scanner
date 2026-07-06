import streamlit as st
import pandas as pd
import requests

# --- TELEGRAM CONFIGURATION ---
TOKEN = "8227355571:AAFb7srp8TE5BbQ_o29Bn7tDCcpnYpYPS9I"
CHAT_ID = "945947285"

def send_telegram_message(message):
    """ടെലിഗ്രാമിലേക്ക് നോട്ടിഫിക്കേഷൻ അയക്കാനുള്ള ഫങ്ക്ഷൻ"""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Telegram Error: {e}")

# --- APP INTERFACE CONFIG ---
st.set_page_config(page_title="Nifty Breakout Scanner", page_icon="🚀", layout="wide")
st.title("🚀 Nifty Breakout Scanner & Alerter")

if "last_alert" not in st.session_state:
    st.session_state.last_alert = ""

# --- SIDEBAR: BROKER API CONFIGURATION ---
st.sidebar.header("🔑 Broker API Settings")
broker = st.sidebar.selectbox(
    "Select Your Broker:",
    options=["Zerodha (Kite)", "Angel One", "Fyers", "Alice Blue"]
)

api_key = st.sidebar.text_input("Enter API Key:", type="password", help="നിങ്ങളുടെ ബ്രോക്കർ പോർട്ടലിൽ നിന്നുള്ള API Key ഇവിടെ നൽകുക")
secret_key = st.sidebar.text_input("Enter Secret Key / Access Token:", type="password")

if st.sidebar.button("🔗 Connect Broker"):
    if api_key and secret_key:
        st.sidebar.success(f"Connected successfully to {broker}!")
    else:
        st.sidebar.error("Please enter both API Key and Secret Key!")

# --- MAIN SCREEN: TIMEFRAME & INDEX SELECTION ---
st.subheader("⚙️ Settings")

# പുതിയ മാറ്റം: ഇൻഡെക്സ് തിരഞ്ഞെടുക്കാനുള്ള സെലക്ട് ബോക്സ്
index_selection = st.selectbox(
    "Select Index:",
    options=["NIFTY", "BANKNIFTY", "FINNIFTY", "MIDCPNIFTY"],
    index=0
)

timeframe = st.selectbox(
    "Select Timeframe for Analysis:",
    options=["15 Minutes", "30 Minutes", "1 Hour"],
    index=0
)

st.write(f"Currently scanning **{index_selection}** in **{timeframe}** mode.")
st.divider()

# --- TEST BUTTON ---
st.subheader("📊 Market Analysis Live Data")
if st.button("🧪 Test Telegram Notification"):
    test_msg = f"🔔 *Test Alert!* \nYour Scanner is successfully connected to @IshstrdeBot! \nIndex: {index_selection}\nTimeframe: {timeframe}\nBroker: {broker}"
    send_telegram_message(test_msg)
    st.success("Test message sent to your Telegram!")

# --- NSE DATA FETCHING FUNCTIONS ---
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9'
}

def get_nse_market_data(symbol):
    """തിരഞ്ഞെടുത്ത ഇൻഡെക്സ് അനുസരിച്ച് ഡാറ്റ ഫെച്ച് ചെയ്യുന്ന ഫങ്ക്ഷൻ"""
    url = f"https://www.nseindia.com/api/option-chain-indices?symbol={symbol}"
    session = requests.Session()
    try:
        session.get("https://www.nseindia.com", headers=headers, timeout=10)
        response = session.get(url, headers=headers, timeout=10)
        return response.json()
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None

st.info(f"{index_selection} ഡാറ്റ അപ്ഡേറ്റ് ചെയ്യാൻ ശ്രമിക്കുന്നു...")
