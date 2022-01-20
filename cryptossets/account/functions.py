
import warnings
import time
import pandas as pd
from typing import Dict, List
from account.models import Info
from coinex.coinex import CoinEx
from kucoin.kucoin.client import Client as Kucoin


STABLE_COINS = ["USDT", "TUSD", "USDC"]


def get_coinex_client(user) -> CoinEx:
    info = Info.objects.get(user=user)
    access_id = info.coinex_access_id
    secret = info.coinex_secret_key
    return CoinEx(access_id, secret)


def get_kucoin_client(user) -> Kucoin:
    info = Info.objects.get(user=user)
    return Kucoin(
        info.kucoin_key,
        info.kucoin_secret,
        info.kucoin_passphrase
    )


def get_market_last_price(user, market: str) -> float:
    response = get_coinex_client(user).market_ticker(market)
    return round(float(response['ticker']['last']), 4)


def get_avg_buy_price(user, market: str) -> float:
    coinex = get_coinex_client(user)
    deals = coinex.order_user_deals(market)['data']
    print(market)

    last_buy_index = len(deals)
    for index, deal in enumerate(deals):
        if deal['type'] == 'sell':
            last_buy_index: int = index
            break

    buy_deals = deals[:last_buy_index]

    total_amount = 0.0
    total_shares = 0.0
    for deal in buy_deals:
        total_amount += float(deal['price']) * float(deal['amount'])
        total_shares += float(deal['amount'])

    if total_shares == 0.0:
        total_shares = 1
    return round(total_amount / total_shares, 4)


def kucoin_get_orders(client) -> List[Dict]:
    start_time: int = 1617222661000
    now = int(round(time.time() * 1000))
    seven_day_in_milisec = 604800000
    orders = []
    while start_time < now:
        _o = client.get_orders(
            start=start_time, end=start_time + seven_day_in_milisec
        )["items"]
        if _o:
            for o in _o:
                orders.append(o)
        start_time += seven_day_in_milisec
        time.sleep(0.2)
    return orders


def kucoin_get_balance(client) -> List[Dict]:
    balance = client.get_accounts()
    balance = filter(lambda b: b["type"] == "trade", balance)
    return list(balance)


def kucoin_calculate(balance: list, orders: list, client) -> List[Dict]:
    data = []
    for b in balance:
        print(b["currency"])
        _data = {}
        _data["name"] = b["currency"]
        _data["balance"] = b["balance"]

        if _data["name"] in STABLE_COINS:
            data.append(
                {
                    "name": _data["name"],
                    "available": round(float(b["balance"]), 4),
                    "last_price": 1.00,
                    "avg_buy_price": 1.00,
                    "capital_involved": round(float(b["balance"]), 4),
                    "market_value": round(float(b["balance"]), 4),
                    "profit_loss": round(float(b["balance"]), 4),
                    "text_color": "black",
                    "percent": 0
                }
            )

            continue

        asset_history = list(
            filter(
                lambda a: a["symbol"].split("-")[0] == b["currency"],
                orders
            )
        )
        df = pd.DataFrame(asset_history, columns=["price", "size", "side"])
        df = df.loc[df["side"] == "buy"]
        df["available"] = df["size"].astype("float")
        df["price"] = df["price"].astype("float")
        df["mul"] = df["price"] * df["available"]
        mul = df["mul"].sum()
        available = float(df["available"].sum())
        with warnings.catch_warnings():
            warnings.filterwarnings("error")
            try:
                _data["avg_buy_price"] = round(mul / available, 2)
            except:
                _data["avg_buy_price"] = float(0)

        _data["available"] = available
        _data["last_price"] = float(
            client.get_ticker(f'{_data["name"]}-USDT')["price"]
        )

        _data['capital_involved'] = round(
            _data['available'] * _data['avg_buy_price'], 2
        )
        _data['market_value'] = round(
            _data['available'] * _data['last_price'], 2
        )

        _data['profit_loss'] = round(
            _data['market_value'] - _data['capital_involved'], 2
        )
        _data["text_color"] = "green" if _data["profit_loss"] >= 0 else "red"
        try:
            _data['percent'] = round(
                (_data['profit_loss'] * 100) / _data['capital_involved'], 2
            )
        except ZeroDivisionError:
            _data['percent'] = 0
        data.append(_data)

        # sample = {
        #     'name': 'ADA',
        #     'available': 134.6728,
        #     'last_price': 1.407,
        #     'avg_buy_price': 2.2155,
        #     'capital_involved': 298.37,
        #     'market_value': 189.4846,
        #     'profit_loss': -108.89,
        #     'percent': -36.49,
        #     'text_color': 'red'
        # }

    return sorted(data, key=lambda i: i.get("profit", 0), reverse=True)
