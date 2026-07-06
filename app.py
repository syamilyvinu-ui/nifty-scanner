import streamlit as st
import pandas as pd
import requests

# --- കോൺഫിഗറേഷൻ ---
# (നിങ്ങളുടെ ടെലിഗ്രാം ടോക്കൺ ഇവിടെ നൽകുക)
TOKEN = "8227355571:AAFb7srp8TE5BbQ_o29Bn7tDCcpnYpYPS9I"
CHAT_ID = "945947285"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

# --- കണക്കുകൂട്ടലുകൾ ---
def calculate_cpr(high, low, close):
    pivot = (high + low + close) / 3
    bc = (high + low) / 2
    tc = (pivot - bc) + pivot
    return tc, pivot, bc

def get_pcr(data):
    # NSE ഡാറ്റയിൽ നിന്ന് Total Put OI, Total Call OI കണ്ടെത്തുക
    try:
        options = data['filtered']['data']
        ce_oi = sum([x['CE']['openInterest'] for x in options if 'CE' in x])
        pe_oi = sum([x['PE']['openInterest'] for x in options if 'PE' in x])
        return pe_oi / ce_oi if ce_oi != 0 else 0
    except:
        return 0

# --- മെയിൻ ആപ്പ് ---
st.set_page_config(page_title="Pro Scanner", layout="wide")
st.title("🚀 Advance CPR & OI Scanner")

power_switch = st.toggle("Power Switch", value=True)

if power_switch:
    index = st.selectbox("Select Index:", ["NIFTY", "BANKNIFTY"])
    
    if st.button("Analyze Market"):
        # 1. ഡാറ്റ ഫെച്ച് ചെയ്യുക (ഉദാഹരണത്തിന്)
        # st.info("ഡാറ്റ വിശകലനം ചെയ്യുന്നു...")
        
        # 2. CPR കണക്കുകൂട്ടുക (നിങ്ങളുടെ ഡാറ്റാ സോഴ്സിൽ നിന്നുള്ള H, L, C വാല്യൂസ് ഉപയോഗിക്കുക)
        # ഉദാഹരണത്തിന് ഇന്നലത്തെ ഹൈ, ലോ, ക്ലോസ്
        h, l, c = 24000, 23800, 23900 
        tc, p, bc = calculate_cpr(h, l, c)
        
        # 3. റിസൾട്ട് കാണിക്കുക
        st.write(f"### {index} Levels")
        st.metric("TC Level", round(tc, 2))
        st.metric("Pivot", round(p, 2))
        st.metric("BC Level", round(bc, 2))
        
        # 4. PCR & Alert
        pcr = 1.15 # മാതൃകയ്ക്ക് വേണ്ടി
        st.progress(pcr / 2, text=f"Current PCR: {pcr}")
        
        if pcr > 1.2:
            msg = f"🔔 *Buy Alert!* {index} is Bullish. PCR: {pcr}"
            send_telegram_message(msg)
            st.success("Bullish Alert Sent!")
else:
    st.warning("Scanner is OFF")
