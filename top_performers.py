import yfinance as yf
import streamlit as st
from datetime import datetime, timedelta

# Fonction pour récupérer les données d'un actif
def get_data(ticker, period="1h", interval="1h"):
    asset = yf.Ticker(ticker+'-USD')
    try:
        data = asset.history(period=period, interval=interval)
        if data.empty:
            raise ValueError(f"No data retrieved for {ticker}.")
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        data = None
    return data

# Fonction pour calculer la performance sur 1 heure
def calculate_performance(data, hours=1):
    if data is None or data.empty:
        raise ValueError("Data is empty. Cannot calculate performance.")

    recent_time = data.index[-1]
    past_time = recent_time - timedelta(hours=hours)

    if past_time in data.index:
        past_price = data.loc[past_time]['Close']
    else:
        past_data = data[data.index <= past_time]
        if past_data.empty:
            raise ValueError("Not enough data to calculate performance.")
        past_price = past_data['Close'].iloc[-1]

    current_price = data.iloc[-1]['Close']
    performance = ((current_price - past_price) / past_price) * 100
    return performance

# Lire la liste des actifs depuis le fichier
with open('/home/kalistan/Desktop/Crypto/cleaned_CSA.txt', 'r') as file:
    tickers = [line.strip() for line in file.readlines()]

# Calculer la performance sur 1 heure pour chaque actif
performances = []
for ticker in tickers:
    data = get_data(ticker, period="1d", interval="1h")
    if data is not None:
        try:
            perf = calculate_performance(data, hours=1)
            performances.append((ticker, perf))
        except ValueError as ve:
            print(f"Error calculating performance for {ticker}: {ve}")

# Trier les actifs par performance décroissante
performances.sort(key=lambda x: x[1], reverse=True)

# Afficher les 10 actifs les plus performants
top_10 = performances[:10]
print("Top 10 actifs les plus performants sur 1 heure :")
st.write("Top 10 actifs les plus performants sur 1 heure :")
for ticker, perf in top_10:
    print(f"{ticker}: {perf:.2f}%")
    st.write(f"{ticker}: {perf:.2f}%")