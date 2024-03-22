import requests
import plotly.graph_objects as go
import streamlit as st
import time

def fetch_ohlc_data(pair, interval=15):
    """Fetch OHLC data for a given pair and interval."""
    url = f"https://api.kraken.com/0/public/OHLC?pair={pair}&interval={interval}"
    response = requests.get(url)
    data = response.json()
    pair_key = next(iter(data['result']), None)  # Safely get the first key
    if pair_key:
        return data['result'][pair_key]
    else:
        return None

def create_ohlc_chart(ohlc_data, pair):
    """Create a Plotly candlestick chart figure for the OHLC data of a given pair."""
    if ohlc_data:
        times = [item[0] for item in ohlc_data]
        opens = [float(item[1]) for item in ohlc_data]
        highs = [float(item[2]) for item in ohlc_data]
        lows = [float(item[3]) for item in ohlc_data]
        closes = [float(item[4]) for item in ohlc_data]

        fig = go.Figure(data=[go.Candlestick(x=times, open=opens, high=highs, low=lows, close=closes)])
        fig.update_layout(title=f"{pair} (15m intervals)",
                          xaxis_title="Time",
                          yaxis_title="Price",
                          xaxis_rangeslider_visible=False)
        return fig
    else:
        return None

# List of currency pairs
pairs = ['SOLUSD', 'ETHUSD', 'XBTUSD', 'FTMUSD']

# Create placeholders for each pair
chart_placeholders = {pair: st.empty() for pair in pairs}

# Update interval (e.g., 60 seconds)
update_interval = 60

while True:
    for pair in pairs:
        ohlc_data = fetch_ohlc_data(pair)
        fig = create_ohlc_chart(ohlc_data, pair)
        if fig:
            chart_placeholders[pair].plotly_chart(fig, use_container_width=True)
        else:
            chart_placeholders[pair].write(f"No data available for {pair}")
    time.sleep(update_interval)  # Wait for the specified interval before fetching new data
