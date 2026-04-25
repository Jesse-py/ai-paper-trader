import argparse
import sys
try:
    import yfinance as yf
    import pandas as pd
except ImportError:
    print("Error: The 'yfinance' or 'pandas' library is not installed. Please install them.")
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Stock Research Tool for AI")
    parser.add_argument('--ticker', type=str, required=True, help="Stock ticker symbol (e.g., AAPL, SPY)")
    args = parser.parse_args()

    ticker_symbol = args.ticker.upper()
    stock = yf.Ticker(ticker_symbol)
    
    try:
        # Get basic info
        info = stock.info
        current_price = info.get('currentPrice', info.get('regularMarketPrice', 'N/A'))
        
        print(f"\n--- 📊 RESEARCH REPORT FOR {ticker_symbol} ---")
        print(f"Company: {info.get('longName', 'N/A')}")
        print(f"Sector: {info.get('sector', 'N/A')} | Industry: {info.get('industry', 'N/A')}")
        print(f"Current Price: ${current_price}")
        print(f"52-Week High: ${info.get('fiftyTwoWeekHigh', 'N/A')}")
        print(f"52-Week Low: ${info.get('fiftyTwoWeekLow', 'N/A')}")
        print(f"Forward P/E: {info.get('forwardPE', 'N/A')}")
        
        # Get last 30 days of history for trend analysis
        print("\n📈 30-DAY TREND & TECHNICAL ANALYSIS:")
        hist = stock.history(period="1mo")
        if not hist.empty:
            # Calculate simple Moving Averages
            hist['SMA_10'] = hist['Close'].rolling(window=10).mean()
            hist['SMA_20'] = hist['Close'].rolling(window=20).mean()
            
            # Calculate 14-Day RSI
            delta = hist['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            hist['RSI_14'] = 100 - (100 / (1 + rs))

            # Calculate 10-Day Average Volume
            hist['Vol_SMA_10'] = hist['Volume'].rolling(window=10).mean()
            
            # Get latest values
            latest = hist.iloc[-1]
            
            # Print Moving Averages
            if not pd.isna(latest['SMA_10']):
                print(f"  10-Day SMA: ${latest['SMA_10']:.2f}")
            if not pd.isna(latest['SMA_20']):
                print(f"  20-Day SMA: ${latest['SMA_20']:.2f}")
                
                if latest['Close'] > latest['SMA_20']:
                    print("  Trend: BULLISH (Price above 20-Day SMA)")
                else:
                    print("  Trend: BEARISH (Price below 20-Day SMA)")
                    
            # Print RSI
            if not pd.isna(latest['RSI_14']):
                print(f"  14-Day RSI: {latest['RSI_14']:.2f} (Over 70 = Overbought, Under 30 = Oversold)")
                
            # Print Volume Data
            if not pd.isna(latest['Vol_SMA_10']):
                print(f"  Today's Volume: {int(latest['Volume']):,} | 10-Day Avg Vol: {int(latest['Vol_SMA_10']):,}")

            # Print last 5 days for immediate context
            print("\n📊 LAST 5 DAYS PRICE HISTORY:")
            for date, row in hist.tail(5).iterrows():
                print(f"  {date.strftime('%Y-%m-%d')}: Close: ${row['Close']:.2f} | Volume: {int(row['Volume']):,}")
        else:
            print("  No recent price history found.")
            
        # Add Recent News Headlines for Sentiment
        print("\n📰 RECENT NEWS:")
        news = stock.news
        if news:
            for item in news[:3]: # Get top 3 articles
                title = item.get('title', 'No Title Available')
                print(f"  - {title}")
        else:
            print("  No recent news articles found.")
            
    except Exception as e:
        print(f"❌ Error fetching data for {ticker_symbol}: {e}")

if __name__ == "__main__":
    main()