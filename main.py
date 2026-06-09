import yfinance as yf
import pandas as pd

# Function to analyse stock
def analyse_stock(ticker, capital):

    # Download stock data
    stock = yf.download(ticker, period="1mo")

    # Yesterday closing price
    yesterday_price = stock['Close'].iloc[-2].item()

    # Today closing price
    today_price = stock['Close'].iloc[-1].item()

    # Daily return
    daily_return = today_price - yesterday_price

    # Shares purchasable
    shares = capital // yesterday_price

    # Estimated total return
    estimated_return = daily_return * shares

    # Return percentage
    return_percentage = (estimated_return / capital) * 100

    return {
        "Ticker": ticker,
        "Yesterday Price": round(yesterday_price, 2),
        "Today Price": round(today_price, 2),
        "Daily Return": round(daily_return, 2),
        "Shares Purchasable": int(shares),
        "Estimated Total Return": round(estimated_return, 2),
        "Return Percentage": round(return_percentage, 2)
    }

# List of Bursa Malaysia stocks
tickers = [
    "1155.KL",   # Maybank
    "1023.KL",   # CIMB
    "5347.KL",   # Tenaga
    "1295.KL",   # Public Bank
    "5183.KL"    # Petronas Chemicals
]

capital = 1000

results = []

# Loop through each stock
for ticker in tickers:
    result = analyse_stock(ticker, capital)
    results.append(result)

# Create DataFrame
df = pd.DataFrame(results)

# Display DataFrame
print("\nBursa Malaysia Stock Analysis")
print(df.to_string(index=False))

# Portfolio Summary Table using slicing
summary = df[[
    "Ticker",
    "Yesterday Price",
    "Today Price",
    "Estimated Total Return",
    "Return Percentage"
]]

print("\nPortfolio Summary Table")
print(summary.to_string(index=False))

# Function to classify performance
def performance_category(x):

    if x < 0:
        return "Negative Return"

    elif x <= 2:
        return "Moderate Return"

    else:
        return "High Return"


# Create new column
df["Performance Category"] = df["Return Percentage"].apply(performance_category)

print("\nPerformance Category Table")
print(df.to_string(index=False))

# GroupBy analysis
grouped = df.groupby("Performance Category")["Estimated Total Return"].mean()

print("\nGroupBy Analysis Result")
print(grouped.to_frame())

import matplotlib.pyplot as plt

# Line chart for stock closing prices
plt.figure(figsize=(10, 6))

for ticker in tickers:

    stock = yf.download(ticker, period="1mo")

    plt.plot(stock.index, stock['Close'], label=ticker)

# Chart details
plt.title("Closing Price Trend of Bursa Malaysia Stocks")
plt.xlabel("Date")
plt.ylabel("Closing Price (RM)")
plt.legend()

# Show chart
plt.savefig("closing_price_trend.png")
plt.show()

# Bar chart for return percentage comparison
plt.figure(figsize=(8, 5))

plt.bar(df["Ticker"], df["Return Percentage"])

# Chart details
plt.title("Return Percentage Comparison")
plt.xlabel("Stock Ticker")
plt.ylabel("Return Percentage (%)")

# Show chart
plt.savefig("return_percentage_comparison.png")
plt.show()
