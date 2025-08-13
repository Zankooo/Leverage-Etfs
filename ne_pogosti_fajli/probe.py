import pandas as pd

# Branje podatkov (brez headerja, ker je tvoj primer surov)
df = pd.read_csv("sp500.csv", header=None, names=["Date", "Close"])

# Pretvori datum
df["Date"] = pd.to_datetime(df["Date"])

# Izračun dnevnih sprememb (returns)
df["DailyChange"] = df["Close"].pct_change()

# 2x leveraged dnevne spremembe
df["DailyChange_2x"] = df["DailyChange"] * 2

# Simulacija cene leveraged indeksa (začnemo pri 100)
start_value = 100
df["Close_2x"] = (1 + df["DailyChange_2x"]).cumprod() * start_value

# Rezultat
print(df)

# Po želji izvoziš v CSV
df.to_csv("sp500_2x.csv", index=False)
