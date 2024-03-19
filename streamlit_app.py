import streamlit as st
import plotly.graph_objects as go
import datetime
from helper_functions import *

if __name__ == "__main__":
    st.title('EuroGrid Trade Viewer')

    trade_numbers_input = st.text_input('Enter trade numbers separated by commas in ascending order (e.g., 0, 94, 203)', value="0")
    try:
        if trade_numbers_input == "":
            raise ValueError("Enter trade number(s)")
        trade_numbers = [int(x.strip()) for x in trade_numbers_input.split(',')]
        if trade_numbers != sorted(trade_numbers):
            raise ValueError("Trade numbers must be in ascending order.")
    except ValueError as e:
        st.error(f"Invalid input: {e}")
        st.stop()

    # Add radio button for timeframe selection
    selected_timeframe = st.radio(
        "Select Timeframe",
        ('1M', '5M', '15M', '1H', '4H', '1D'),
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

    desired_columns = [
        'Open DateTime', 'Opening Price', 'Type', 'Volume',
        'S / L', 'T / P', 'Close DateTime', 'Closing Price'
    ]

    trade_data_dfs = []  # List to hold individual trade data DataFrames
    for trade_number in trade_numbers:
        trade_data_file_path = 'trades/trade_' + str(trade_number) + '.csv'
        trade_data_df = load_trade_data(trade_data_file_path)
        trade_data_df = trade_data_df[desired_columns]
        trade_data_dfs.append(trade_data_df)
    if not trade_data_dfs:
        st.write("No valid trades selected.")
        st.stop()
    
    tick_data_file_path = file_mapping[selected_timeframe]
    tf_ohlc_data = load_tick_data(tick_data_file_path)

    # Inputting display settings
    input_settings = {}
    input_settings["Candles Before"] = st.number_input('Candles Before Trade', min_value=0, value=5)
    input_settings["Candles After"] = st.number_input('Candles After Trade', min_value=0, value=5)
    input_settings["Showing Position Lot Size"] = st.toggle('Show Position Lot Size?')
    input_settings["Showing Hedges"] = st.toggle('Show Hedges?', value=True)

    # Indicator settings
    input_settings["Display RSI?"] = st.toggle("Display RSI?", value=False)
    if input_settings["Display RSI?"]:
        input_settings["RSI Length"] = st.number_input("RSI Length", value=21, min_value=1)

    input_settings["Display Bollinger Bands?"] = st.toggle('Display Bollinger Bands?', value=False)
    if input_settings["Display Bollinger Bands?"]:
        input_settings["Bollinger Bands Period"] = st.number_input('Bollinger Bands Period', min_value=1, value=20)
        input_settings["Bollinger Bands Std. Dev"] = st.number_input('Bollinger Bands Std. Dev', value=2)

    trade_agg_data = pd.concat(trade_data_dfs).reset_index(drop=True)
    if not input_settings["Showing Hedges"]:
        trade_agg_data = filter_initial_trades(trade_agg_data)
        trade_agg_data = trade_agg_data[desired_columns]

    chart = create_candlestick_chart(
        tf_ohlc_data,
        trade_agg_data,
        selected_timeframe,
        input_settings
    )
    st.plotly_chart(chart, use_container_width=True)

    st.table(trade_agg_data)