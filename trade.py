import argparse
import os
import sys

try:
    from alpaca.trading.client import TradingClient
    from alpaca.trading.requests import MarketOrderRequest
    from alpaca.trading.enums import OrderSide, TimeInForce
except ImportError:
    print("Error: The 'alpaca-py' library is not installed. Please install it.")
    sys.exit(1)

def main():
    # Set up command-line arguments so Claude can trigger specific actions
    parser = argparse.ArgumentParser(description="Alpaca Paper Trading CLI for AI")
    parser.add_argument('--portfolio', action='store_true', help="View account balances and open positions")
    parser.add_argument('--action', choices=['buy', 'sell'], help="Action to perform (buy or sell)")
    parser.add_argument('--ticker', type=str, help="Stock ticker symbol (e.g., AAPL)")
    parser.add_argument('--qty', type=float, help="Quantity of shares to trade")
    
    args = parser.parse_args()

    # The script looks for API keys in the environment variables
    api_key = os.getenv("APCA_API_KEY_ID")
    secret_key = os.getenv("APCA_API_SECRET_KEY")

    if not api_key or not secret_key:
        print("CRITICAL ERROR: Missing Alpaca API keys.")
        print("Please set APCA_API_KEY_ID and APCA_API_SECRET_KEY as environment variables.")
        sys.exit(1)

    # Initialize the Trading Client (paper=True ensures we are using fake money!)
    client = TradingClient(api_key, secret_key, paper=True)

    # COMMAND: View Portfolio
    if args.portfolio:
        try:
            account = client.get_account()
            print("\n" + "="*30)
            print("💰 PORTFOLIO SUMMARY")
            print("="*30)
            print(f"Total Equity:   ${float(account.equity):.2f}")
            print(f"Buying Power:   ${float(account.buying_power):.2f}")
            print(f"Cash Available: ${float(account.cash):.2f}")
            
            print("\n" + "="*30)
            print("📊 OPEN POSITIONS")
            print("="*30)
            positions = client.get_all_positions()
            
            if not positions:
                print("No open positions currently held.")
            else:
                for p in positions:
                    profit_loss = float(p.unrealized_pl)
                    pl_sign = "+" if profit_loss >= 0 else ""
                    print(f"TICKER: {p.symbol}")
                    print(f"  Shares: {p.qty}")
                    print(f"  Avg Entry: ${float(p.avg_entry_price):.2f} | Current: ${float(p.current_price):.2f}")
                    print(f"  Total P/L: {pl_sign}${profit_loss:.2f}")
                    print("-" * 20)
            return
            
        except Exception as e:
            print(f"Error fetching portfolio data: {e}")
            sys.exit(1)

    # COMMAND: Execute Trade
    if args.action and args.ticker and args.qty:
        try:
            side = OrderSide.BUY if args.action == 'buy' else OrderSide.SELL
            
            # Create a market order
            order_data = MarketOrderRequest(
                symbol=args.ticker.upper(),
                qty=args.qty,
                side=side,
                time_in_force=TimeInForce.DAY # Automatically cancels at end of day if unfilled
            )
            
            # Submit the order
            order = client.submit_order(order_data=order_data)
            
            print(f"✅ SUCCESS! ORDER SUBMITTED.")
            print(f"Action: {args.action.upper()}")
            print(f"Ticker: {args.ticker.upper()}")
            print(f"Quantity: {args.qty}")
            print(f"Order ID: {order.id}")
            print(f"Status: {order.status.value}")
            return
            
        except Exception as e:
            print(f"❌ FAILED TO SUBMIT ORDER: {e}")
            sys.exit(1)
            
    # If no valid arguments were passed
    print("Invalid command. Please specify an action.")
    print("Examples:")
    print("  python trade.py --portfolio")
    print("  python trade.py --action buy --ticker AAPL --qty 5")

if __name__ == "__main__":
    main()