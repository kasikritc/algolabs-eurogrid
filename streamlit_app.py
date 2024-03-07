import streamlit as st
import plotly.graph_objects as go
import datetime
from helper_functions import *

if __name__ == "__main__":
    st.title('Trade Data and Candlestick Chart Viewer')

    # Add radio button for timeframe selection
    selected_timeframe = st.radio(
        "Select Timeframe",
        ('1M', '5M', '15M', '1H', '4H', '1D')
    )

    # Map the selection to the corresponding file
    file_mapping = {
        '1M': '1M_XAUUSD_OHLC_dropna.csv',
        '5M': '5M_XAUUSD_OHLC_dropna.csv',
        '15M': '15M_XAUUSD_OHLC_dropna.csv',
        '1H': '1H_XAUUSD_OHLC_dropna.csv',
        '4H': '4H_XAUUSD_OHLC_dropna.csv',
        '1D': '1D_XAUUSD_OHLC_dropna.csv'
    }

    trade_data_file_path = 'clean_trade_data.csv'
    tick_data_file_path = file_mapping[selected_timeframe]
    trade_data = load_trade_data(trade_data_file_path)
    tf_ohlc_data = load_tick_data(tick_data_file_path)

    # Organizing the dataframe
    desired_columns = [
        'Trade Number', 'Open DateTime', 'Price', 'Type', 
        'S / L', 'T / P', 'Close DateTime', 'Price.1'
    ]
    trade_data = trade_data[desired_columns]
    trade_data.rename(columns={
        'Price': 'Open Price',
        'Price.1': 'Close Price'
    }, inplace=True)

    selected_trades = select_trades_by_number(trade_data)

    # Inputting display settings
    input_settings = {}
    input_settings["Candles Before"] = st.number_input('Candles Before Trade', min_value=0, value=5)
    input_settings["Candles After"] = st.number_input('Candles After Trade', min_value=0, value=5)

    # Initialize an empty dictionary to store the user's choices
    yesterday_ohlc_questions = ["Display yesterday's high?", 
                                "Display yesterday's low?",
                                "Display yesterday's open?",
                                "Display yesterday's close?"]
    for question in yesterday_ohlc_questions:
        input_settings[question] = st.toggle(question)
    if any(input_settings[key] for key in yesterday_ohlc_questions):
        input_settings["Daily OHLC Data"] = load_tick_data(file_mapping['1D'])

    input_settings["Display RSI?"] = st.toggle("Display RSI?", value=True)
    if input_settings["Display RSI?"]:
        input_settings["RSI Length"] = st.number_input("RSI Length", value=21, min_value=1)

    rows, cols = selected_trades.shape
    if rows != 0:
        chart = create_candlestick_chart(
            tf_ohlc_data,
            selected_trades,
            selected_timeframe,
            input_settings
        )
        st.plotly_chart(chart, use_container_width=True)
    else:
        for _ in range(3):
            st.write("")
        st.write("No trade selected")