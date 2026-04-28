# AI Trading Journal
*Goal: Make the most money possible.*

## Initial Setup
- Starting paper balance: $100,000
- Initial strategy: TBD by AI.
---
Date: 2026-04-28
Post-Mortem: First day of operation. Portfolio could not be retrieved — Alpaca API returned `{"message": "unauthorized."}` for both `--portfolio` and `--action buy` calls despite APCA_API_KEY_ID and APCA_API_SECRET_KEY being present in the environment. No prior trades to evaluate.
Market Snapshot:
- SPY: $712.02, RSI 79.58 (overbought), trend bullish but at 52-wk high ($715.63). Volume 26.8M vs 10d avg 48.5M (declining participation).
- AAPL: $270.32, RSI 62.36, trend bullish, well below 52-wk high ($288.62). Healthier momentum, room to run.
- NVDA: $214.53, RSI 84.01 (extremely overbought), at 52-wk high. Avoid chasing.
Rule Adjustment: Establishing initial strategy. Will not buy assets with RSI > 70 (avoid chasing tops). Will avoid concentrating in mega-cap tech that is already at 52-wk highs. Position sizing capped at 10% of equity per trade.
Actions Taken: NONE — API authentication failure prevented all trade execution. User must verify Alpaca paper trading API keys.
Forward Strategy: If API access is restored tomorrow:
  1. First check portfolio for available cash and any positions.
  2. If SPY pulls back and RSI drops to 60-65 range, consider broad market exposure.
  3. AAPL is the most attractive candidate among researched names — RSI 62, not at 52-wk high, bullish trend, sub-30 forward P/E.
  4. Avoid NVDA at RSI 84 — wait for pullback below RSI 70.
  5. Watch volume trends — declining volume on rising prices is a distribution warning.
