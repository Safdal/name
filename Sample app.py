from kiteconnect import KiteConnect, KiteTicker
import datetime

# API credentials (replace with your API Key and Access Token)
api_key = "your_api_key"
api_secret = "your_api_secret"
access_token = "your_access_token"

kite = KiteConnect(api_key=api_key)
kite.set_access_token(access_token)

# Trading parameters
stock = "RELIANCE"  # Reliance Industries Ltd.
exchange = "NSE"    # National Stock Exchange
stoploss_pct = 0.7  # 0.7% stop-loss
target_pct = 1.5    # 1.5% target

def place_orders():
    ltp = kite.ltp(f"{exchange}:{stock}")[f"{exchange}:{stock}"]["last_price"]

    # Calculate stop-loss and target
    buy_sl = round(ltp * (1 - stoploss_pct / 100), 2)
    buy_target = round(ltp * (1 + target_pct / 100), 2)
    sell_sl = round(ltp * (1 + stoploss_pct / 100), 2)
    sell_target = round(ltp * (1 - target_pct / 100), 2)

    # Place Buy Order
    kite.place_order(
        tradingsymbol=stock,
        exchange=exchange,
        transaction_type="BUY",
        quantity=1,
        order_type="MARKET",
        product="MIS",  # Intraday
        variety="regular"
    )

    # Place Short Sell Order
    kite.place_order(
        tradingsymbol=stock,
        exchange=exchange,
        transaction_type="SELL",
        quantity=1,
        order_type="MARKET",
        product="MIS",  # Intraday
        variety="regular"
    )

    print(f"Orders placed at {ltp}. Targets: {buy_target}, {sell_target}")

def main():
    now = datetime.datetime.now()
    market_open_time = datetime.time(9, 30)
    
    # Run the script only if the market is open
    if now.time() >= market_open_time:
        place_orders()

if __name__ == "__main__":
    main()
