# Qur'anic Resonance Trading Strategy (QRTS) - Web GUI using Streamlit
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="QRTS Web App", layout="centered")
st.title("Qur'anic Resonance Trading Strategy (QRTS)")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df['date'] = pd.to_datetime(df['date'])

    tickers = df['Name'].unique().tolist()
    selected_ticker = st.selectbox("Select a stock ticker", tickers)

    F = st.slider("Sacred Frequency (F)", 0.1, 1.0, 0.432)
    T = st.slider("Golden Ratio Time (T)", 1.0, 3.0, 1.618**2)
    C = st.slider("Coherence Index (C)", 0.5, 1.0, 0.85)
    R = np.pi / 2

    df_ticker = df[df['Name'] == selected_ticker].copy()
    df_ticker = df_ticker.sort_values('date')
    df_ticker.set_index('date', inplace=True)

    df_ticker['Return'] = df_ticker['close'].pct_change()
    time_index = np.arange(len(df_ticker))
    df_ticker['Signal'] = np.sin(F * T * time_index) * np.cos(R * time_index)

    df_ticker['TradeSignal'] = 0
    df_ticker.loc[(df_ticker['Signal'] > C) & (df_ticker['Return'] > 0), 'TradeSignal'] = 1
    df_ticker.loc[(df_ticker['Signal'] < -C) & (df_ticker['Return'] < 0), 'TradeSignal'] = -1

    df_ticker['StratReturn'] = df_ticker['TradeSignal'].shift(1) * df_ticker['Return']
    df_ticker['QRT'] = (1 + df_ticker['StratReturn']).cumprod()
    df_ticker['BuyHold'] = (1 + df_ticker['Return']).cumprod()

    st.subheader(f"QRTS vs Buy & Hold for {selected_ticker}")
    fig, ax = plt.subplots()
    df_ticker[['QRT', 'BuyHold']].plot(ax=ax)
    st.pyplot(fig)

    st.subheader("Final Performance")
    st.write(df_ticker[['QRT', 'BuyHold']].iloc[-1])
