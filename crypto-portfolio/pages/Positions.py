import streamlit as st
import time
import os
import requests
import hashlib
import hmac
import base64
from urllib.parse import urlencode
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Your API credentials
api_url = "https://api.kraken.com"
api_key = os.getenv("KRAKEN_API_KEY")
api_sec = os.getenv("KRAKEN_API_SECRET")

def get_kraken_signature(urlpath, data, secret):
    postdata = urlencode(data)
    encoded = (str(data["nonce"]) + postdata).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()
    mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
    sigdigest = base64.b64encode(mac.digest())
    return sigdigest.decode()

def kraken_request(uri_path, data, api_key, api_sec):
    headers = {'API-Key': api_key, 'API-Sign': get_kraken_signature(uri_path, data, api_sec)}
    response = requests.post(api_url + uri_path, headers=headers, data=data)
    return response

def fetch_last_trades(api_key, api_sec, count=10):
    uri_path = "/0/private/TradesHistory"
    data = {
        "nonce": str(int(time.time() * 1000)),
        "trades": True
    }
    response = kraken_request(uri_path, data, api_key, api_sec).json()
    if response and 'result' in response and 'trades' in response['result']:
        trades = list(response['result']['trades'].values())[-count:]
        return trades
    else:
        st.error("Failed to extract trades from response.")
        return []

def display_trades(trades):
    if trades:
        st.write("### Last 10 Trades")
        for trade in trades:
            st.json(trade)
    else:
        st.write("No trades to display.")


def main():
    st.title("Kraken Last 10 Trades")
    try:
        # Directly use api_key and api_sec from the global scope
        last_trades = fetch_last_trades(api_key, api_sec)
        display_trades(last_trades)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
