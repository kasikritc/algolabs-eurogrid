import streamlit as st
import plotly.graph_objects as go
import datetime
from helper_functions import *

if __name__ == "__main__":
    st.title('Trade Data and Candlestick Chart Viewer')

    trade_number = int(st.number_input('Choose trade number', value=0, min_value=0, max_value=1758, step=1))

    # Add radio button for timeframe selection
    selected_timeframe = st.radio(
        "Select Timeframe",
        ('1M', '5M', '15M', '1H', '4H', '1D')
    )

    # Map the selection to the corresponding file
    file_mapping = {
        '1M': '1M_EURUSD_OHLC_dropna.csv',
        '5M': '5M_EURUSD_OHLC_dropna.csv',
        '15M': '15M_EURUSD_OHLC_dropna.csv',
        '1H': '1H_EURUSD_OHLC_dropna.csv',
        '4H': '4H_EURUSD_OHLC_dropna.csv',
        '1D': '1D_EURUSD_OHLC_dropna.csv'
    }

    trade_data_file_path = 'trades/trade_' + str(trade_number) + '.csv'
    tick_data_file_path = file_mapping[selected_timeframe]
    trade_data = load_trade_data(trade_data_file_path)
    tf_ohlc_data = load_tick_data(tick_data_file_path)

    # Organizing the dataframe
    desired_columns = [
        'Open DateTime', 'Opening Price', 'Type', 'Volume',
        'S / L', 'T / P', 'Close DateTime', 'Closing Price'
    ]
    trade_data = trade_data[desired_columns]

    # Inputting display settings
    input_settings = {}
    input_settings["Candles Before"] = st.number_input('Candles Before Trade', min_value=0, value=5)
    input_settings["Candles After"] = st.number_input('Candles After Trade', min_value=0, value=5)
    input_settings["Showing Position Lot Size"] = st.toggle('Show Position Lot Size?')
    input_settings["Showing Hedges"] = st.toggle('Show Hedges?', value=True)

    rows, cols = trade_data.shape
    if rows != 0:
        chart = create_candlestick_chart(
            tf_ohlc_data,
            trade_data,
            selected_timeframe,
            input_settings
        )
        st.plotly_chart(chart, use_container_width=True)
    else:
        for _ in range(3):
            st.write("")
        st.write("No trade selected")
    
    st.table(trade_data)