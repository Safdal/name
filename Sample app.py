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
trailing_stop = 2   # 2 points trailing stop-loss

def place_orders():
    ltp = kite.ltp(f"{exchange}:{stock}")[f"{exchange}:{stock}"]["last_price"]

    # Calculate initial stop-loss and target
    buy_sl = round(ltp * (1 - stoploss_pct / 100), 2)
    buy_target = round(ltp * (1 + target_pct / 100), 2)
    sell_sl = round(ltp * (1 + stoploss_pct / 100), 2)
    sell_target = round(ltp * (1 - target_pct / 100), 2)

    # Place Buy Order
    buy_order = kite.place_order(
        tradingsymbol=stock,
        exchange=exchange,
        transaction_type="BUY",
        quantity=1,
        order_type="MARKET",
        product="MIS",  # Intraday
        variety="regular"
    )

    # Place Short Sell Order
    sell_order = kite.place_order(
        tradingsymbol=stock,
        exchange=exchange,
        transaction_type="SELL",
        quantity=1,
        order_type="MARKET",
        product="MIS",  # Intraday
        variety="regular"
    )

    print(f"Orders placed at {ltp}. Targets: {buy_target}, {sell_target}")

    # Monitor the orders and apply trailing stop-loss
    track_trailing_stop(buy_order, sell_order, ltp)

def track_trailing_stop(buy_order, sell_order, ltp):
    # Track Buy Order
    buy_trailing_stop = ltp - trailing_stop
    print(f"Initial trailing stop for buy order: {buy_trailing_stop}")

    # Track Short Sell Order
    sell_trailing_stop = ltp + trailing_stop
    print(f"Initial trailing stop for sell order: {sell_trailing_stop}")

    while True:
        current_price = kite.ltp(f"{exchange}:{stock}")[f"{exchange}:{stock}"]["last_price"]

        # Update trailing stop for Buy Order if price moves in favor
        if current_price > ltp:
            buy_trailing_stop = max(buy_trailing_stop, current_price - trailing_stop)
            print(f"Updated trailing stop for buy: {buy_trailing_stop}")

        # Update trailing stop for Short Sell Order if price moves in favor
        elif current_price < ltp:
            sell_trailing_stop = min(sell_trailing_stop, current_price + trailing_stop)
            print(f"Updated trailing stop for sell: {sell_trailing_stop}")

        # Check if stop-loss is hit
        if current_price <= buy_trailing_stop:
            print(f"Buy order stop-loss triggered at {current_price}")
            # You can place a sell order here to close the buy position if desired

        if current_price >= sell_trailing_stop:
            print(f"Sell order stop-loss triggered at {current_price}")
            # You can place a buy order here to close the short sell position if desired

def main():
    now = datetime.datetime.now()
    market_open_time = datetime.time(9, 30)
    
    # Run the script only if the market is open
    if now.time() >= market_open_time:
        place_orders()

if __name__ == "__main__":
    main()
