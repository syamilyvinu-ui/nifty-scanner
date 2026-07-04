import streamlit as st
import pandas as pd
import requests
import time

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

# --- APP INTERFACE ---
st.set_page_config(page_title="Nifty Breakout Scanner", page_icon="🚀", layout="wide")
st.title("🚀 Nifty Breakout Scanner & Alerter")

# സെഷൻ സ്റ്റേറ്റ് (മുൻപ് അയച്ച മെസ്സേജുകൾ വീണ്ടും വീണ്ടും അയക്കാതിരിക്കാൻ)
if "last_alert" not in st.session_state:
    st.session_state.last_alert = ""

# --- TIMEFRAME SELECTION (പുതിയ ഫീച്ചർ) ---
st.subheader("⚙️ Settings")
timeframe = st.selectbox(
    "Select Timeframe for Analysis:",
    options=["15 Minutes", "30 Minutes", "1 Hour"],
    index=0
)

st.write(f"Currently scanning in **{timeframe}** mode.")

# --- DATA FETCHING & LOGIC (EXAMPLE PLACEHOLDER) ---
# ഇവിടെയാണ് നിങ്ങളുടെ യഥാർത്ഥ NSE Live Data / OI Analysis കോഡ് വരേണ്ടത്.
# ഉദാഹരണത്തിന് ഒരു ബ്രേക്ക്ഔട്ട് കണ്ടുപിടിക്കുന്ന ഭാഗം താഴെ നൽകുന്നു:

st.divider()
st.subheader("📊 Market Analysis Live Data")

# ടെസ്റ്റിംഗിനായി ഒരു ബട്ടൺ (ഇത് ഞെക്കിയാൽ ഇപ്പോൾ തന്നെ ടെലിഗ്രാമിൽ മെസ്സേജ് വരും)
if st.button("🧪 Test Telegram Notification"):
    test_msg = f"🔔 *Test Alert!* \nYour Nifty Scanner is successfully connected to @IshstrdeBot! \nTimeframe: {timeframe}"
    send_telegram_message(test_msg)
    st.success("Test message sent to your Telegram!")

# --- LIVE MARKET BREAKOUT LOGIC (തിങ്കളാഴ്ച റൺ ചെയ്യാൻ) ---
# നിങ്ങളുടെ യഥാർത്ഥ കണ്ടീഷൻ ഇവിടെ കൊടുക്കാം. (ഉദാഹരണം:)
breakout_detected = False 
breakout_details = ""

if breakout_detected:
    alert_text = f"🚨 *NIFTY BREAKOUT ALERT ({timeframe})* 🚨\nPrice crossed major level! Check your broker app now."
    
    # ഒരേ അലേർട്ട് വീണ്ടും വീണ്ടും അയക്കാതിരിക്കാൻ
    if st.session_state.last_alert != alert_text:
        send_telegram_message(alert_text)
        st.session_state.last_alert = alert_text
        st.bell() # ഫോണിൽ ഒരു ചെറിയ ശബ്ദം വരാൻ

st.info("NSE ഡാറ്റ അപ്ഡേറ്റ് ചെയ്യാൻ ശ്രമിക്കുന്നു... (തിങ്കളാഴ്ച രാവിലെ 9:15 മുതൽ ലൈവ് ഡാറ്റ ലഭ്യമാകും)")
                total_volume += call_vol
                oi_list.append({'strike': strike, 'call_oi': call_oi, 'put_oi': put_oi})
                
        df_oi = pd.DataFrame(oi_list)
        highest_call_strike = df_oi.loc[df_oi['call_oi'].idxmax()]['strike']
        underlying_value = data['records']['underlyingValue']
        current_total_oi = df_oi['call_oi'].sum() + df_oi['put_oi'].sum()
        
        return highest_call_strike, underlying_value, current_total_oi, total_volume
    except:
        return None, None, None, None

# ആപ്പ് മെമ്മറി സെറ്റപ്പ് (മുൻപത്തെ ഡാറ്റ സൂക്ഷിക്കാൻ)
if 'prev_price' not in st.session_state: st.session_state.prev_price = 0
if 'prev_oi' not in st.session_state: st.session_state.prev_oi = 0
if 'prev_vol' not in st.session_state: st.session_state.prev_vol = 0

placeholder = st.empty()

while True:
    resistance, live_price, live_oi, live_vol = get_nse_market_data()
    
    with placeholder.container():
        if resistance and live_price and live_oi and live_vol:
            
            # ലൈവ് ഡാറ്റ ബോക്സുകൾ
            col1, col2 = st.columns(2)
            col1.metric("Nifty Live Price", f"₹{live_price:.2f}")
            col2.metric("Resistance (High Call OI)", int(resistance))
            
            # കംപ്ലീറ്റ് കണ്ടീഷൻ ചെക്കിങ്
            if (live_price > resistance) and (live_oi > st.session_state.prev_oi) and (live_vol > st.session_state.prev_vol):
                st.success(f"🚀🚀 BREAKOUT SIGNAL: BUY CALL (CE) 🚀\n\nവില: {live_price:.2f}\nകാരണം: റെസിസ്റ്റൻസ് കട്ട് ചെയ്തു + OI വർദ്ധിച്ചു + Volume വർദ്ധിച്ചു! (Strong Long Buildup)")
                
            elif (live_price < resistance) and st.session_state.prev_price >= resistance:
                # റെസിസ്റ്റൻസിൽ തട്ടി താഴേക്ക് വരുമ്പോൾ (റിവേഴ്സൽ)
                st.error(f"🚨🚨 REVERSAL SIGNAL: BUY PUT (PE) 🚨\n\nവില: {live_price:.2f}\nകാരണം: റെസിസ്റ്റൻസിൽ നിന്ന് വില താഴേക്ക് തിരിയുന്നു!")
            else:
                st.info("⌛ മാർക്കറ്റ് നിരീക്ഷിക്കുന്നു... മൂവ്മെന്റുകൾക്കായി കാത്തിരിക്കുന്നു.")
            
            # മുൻപത്തെ വാല്യൂസ് അപ്ഡേറ്റ് ചെയ്യുന്നു
            st.session_state.prev_price = live_price
            st.session_state.prev_oi = live_oi
            st.session_state.prev_vol = live_vol
        else:
            st.warning("NSE ഡാറ്റ അപ്ഡേറ്റ് ചെയ്യാൻ ശ്രമിക്കുന്നു...")
            
    time.sleep(30) # ഓരോ 30 സെക്കൻഡിലും സ്കാൻ ചെയ്യും
