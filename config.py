"""
=========================================
ISHA TRADE
CONFIG FILE
=========================================
"""

# -----------------------------
# APP SETTINGS
# -----------------------------
APP_NAME = "ISHA TRADE"

REFRESH_SECONDS = 60

DEFAULT_INDEX = "NIFTY"

DEFAULT_TIMEFRAME = "15m"

# -----------------------------
# BROKER SETTINGS
# -----------------------------
BROKER = "NSE"

API_KEY = ""

API_SECRET = ""

CLIENT_ID = ""

ACCESS_TOKEN = ""

TOTP = ""

# -----------------------------
# TELEGRAM SETTINGS
# -----------------------------
BOT_TOKEN = ""

CHAT_ID = ""

# -----------------------------
# INDEX SYMBOLS
# -----------------------------
INDEX_SYMBOLS = {

    "NIFTY": "^NSEI",

    "BANKNIFTY": "^NSEBANK",

    "FINNIFTY": "NIFTY_FIN_SERVICE.NS",

    "SENSEX": "^BSESN"

}

# -----------------------------
# TIMEFRAMES
# -----------------------------
TIMEFRAMES = {

    "15m": "15m",

    "30m": "30m",

    "60m": "60m"

}

# -----------------------------
# RSI SETTINGS
# -----------------------------
RSI_PERIOD = 14

RSI_CALL_LEVEL = 40

RSI_PUT_LEVEL = 70

# -----------------------------
# EMA SETTINGS
# -----------------------------
EMA_FAST = 14

EMA_SLOW = 20

# -----------------------------
# OPTION SETTINGS
# -----------------------------
ATM_RANGE = 2

LOT_SIZE = {

    "NIFTY": 75,

    "BANKNIFTY": 35,

    "FINNIFTY": 40,

    "SENSEX": 20

}
