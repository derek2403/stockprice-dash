import streamlit as st
import yfinance as yf
import pandas as pd

st.title("Interactive Financial Simulation")

st.sidebar.header("Simulation Settings")

ticker = st.sidebar.text_input("Stock Ticker", value="AAPL")

investment_amount = st.sidebar.number_input("Investment Amount ($)", value=1000, min_value=100)

simulation_period = st.sidebar.slider("Simulation Period (years)", 1, 10, value=1)

@st.cache
def fetch_stock_data(ticker):
    stock_data = yf.download(ticker, period=f"{simulation_period}y", interval="1d")
    return stock_data

stock_data = fetch_stock_data(ticker)

if stock_data.empty:
    st.error("Invalid Stock Ticker or no data available")
else:
    st.subheader(f"Stock Data for {ticker}")
    st.line_chart(stock_data['Close'])

    initial_price = stock_data['Close'][0]
    final_price = stock_data['Close'][-1]
    num_shares = investment_amount / initial_price
    final_value = num_shares * final_price
    profit_loss = final_value - investment_amount

    st.subheader("Investment Summary")
    st.write(f"Initial Price: ${initial_price:.2f}")
    st.write(f"Final Price: ${final_price:.2f}")
    st.write(f"Number of Shares: {num_shares:.2f}")
    st.write(f"Final Value: ${final_value:.2f}")
    st.write(f"Profit/Loss: ${profit_loss:.2f}")

    st.subheader("Interactive Investment Simulation")
    st.line_chart(stock_data['Close'])
    st.write("Use the slider to simulate different investment periods.")
    investment_period = st.slider("Investment Period (days)", 1, len(stock_data), value=30)
    
    initial_price_period = stock_data['Close'][0]
    final_price_period = stock_data['Close'][investment_period-1]
    final_value_period = num_shares * final_price_period
    profit_loss_period = final_value_period - investment_amount

    st.write(f"Initial Price for period: ${initial_price_period:.2f}")
    st.write(f"Final Price for period: ${final_price_period:.2f}")
    st.write(f"Final Value for period: ${final_value_period:.2f}")
    st.write(f"Profit/Loss for period: ${profit_loss_period:.2f}")
