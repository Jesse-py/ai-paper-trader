import argparse
import sys
try:
    import yfinance as yf
except ImportError:
    print("Error: The 'yfinance' library is not installed. Please install it.")
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
        
        # Get last 5 days of history for trend analysis
        print("\n📈 LAST 5 DAYS PRICE HISTORY:")
        hist = stock.history(period="5d")
        if not hist.empty:
            # Format the output so it's easy for the AI to read
            for date, row in hist.iterrows():
                print(f"  {date.strftime('%Y-%m-%d')}: Close: ${row['Close']:.2f} | Volume: {int(row['Volume'])}")
        else:
            print("  No recent price history found.")
            
    except Exception as e:
        print(f"❌ Error fetching data for {ticker_symbol}: {e}")

if __name__ == "__main__":
    main()