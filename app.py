import streamlit as st
from scanner import get_market_analysis # scanner.py-യിൽ നിന്ന് ഫങ്ഷൻ എടുക്കുന്നു

# ... (മറ്റ് കോഡുകൾ)

if st.button("Start Signal Scanner"):
    while True:
        ltp, signal = get_market_analysis(index) # ഇവിടെയാണ് scanner.py പ്രവർത്തിക്കുന്നത്
        st.write(f"Price: {ltp} | Signal: {signal}")
        
        if signal != "NEUTRAL":
            send_telegram(f"🔔 ALERT: {index} -> {signal} at {ltp}")
        
        time.sleep(60)
        st.rerun()
