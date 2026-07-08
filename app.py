import streamlit as st
from datetime import datetime
import pytz

# Scanner Functions
from scanner import (
    get_index_price,
    get_option_chain,
    get_signal
)

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="ISHA TRADE",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------------------------------------
# CUSTOM CSS
# -------------------------------------------------
st.markdown("""
<style>

.main{
    background:#0e1117;
}

.title{
    text-align:center;
    color:#00ff88;
    font-size:38px;
    font-weight:bold;
}

.sub{
    text-align:center;
    color:white;
    font-size:18px;
}

.box{
    background:#1b1f24;
    padding:15px;
    border-radius:10px;
    border:1px solid #333;
}

.signal{
    text-align:center;
    font-size:32px;
    font-weight:bold;
    color:#00ff88;
}

</style>
""",unsafe_allow_html=True)

# -------------------------------------------------
# DATE & TIME
# -------------------------------------------------
india = pytz.timezone("Asia/Kolkata")

now = datetime.now(india)

date = now.strftime("%d-%m-%Y")

time = now.strftime("%I:%M:%S %p")

# -------------------------------------------------
# HEADER
# -------------------------------------------------
st.markdown(
    "<div class='title'>ISHA TRADE</div>",
    unsafe_allow_html=True
)

st.markdown(
    f"<div class='sub'>{date} | {time}</div>",
    unsafe_allow_html=True
)

st.divider()

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------
with st.sidebar:

    st.title("⚙ SETTINGS")

    broker = st.selectbox(
        "Broker",
        [
            "NSE",
            "Zerodha",
            "Angel One",
            "Upstox",
            "Dhan",
            "Shoonya"
        ]
    )

    api_key = st.text_input(
        "API KEY"
    )

    api_secret = st.text_input(
        "API SECRET",
        type="password"
    )

    client_id = st.text_input(
        "CLIENT ID"
    )

    access_token = st.text_input(
        "ACCESS TOKEN"
    )

    totp = st.text_input(
        "TOTP / Secret Code",
        type="password"
    )
