import streamlit as st
import pandas as pd
import requests
import time

# ആപ്പ് സെറ്റിങ്സ്
st.set_page_config(page_title="Nifty Breakout Scanner", page_icon="🚀", layout="centered")
st.title("🚀 Nifty 50 Breakout & OI Scanner")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9'
}

def get_nse_market_data():
    url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"
    session = requests.Session()
    try:
        session.get("https://www.nseindia.com", headers=headers, timeout=10)
        response = session.get(url, headers=headers, timeout=10)
        data = response.json()
        
        records = data['records']['data']
        current_expiry = data['records']['expiryDates'][0]
        
        oi_list = []
        total_volume = 0
        
        for row in records:
            if row.get('expiryDate') == current_expiry:
                strike = row.get('strikePrice')
                call_oi = row.get('CE', {}).get('openInterest', 0) if row.get('CE') else 0
                call_vol = row.get('CE', {}).get('totalTradedVolume', 0) if row.get('CE') else 0
                put_oi = row.get('PE', {}).get('openInterest', 0) if row.get('PE') else 0
                
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
