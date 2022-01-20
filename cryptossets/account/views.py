from django.shortcuts import render
from account.functions import (
    get_coinex_client, get_kucoin_client, get_market_last_price, get_avg_buy_price,
    kucoin_calculate, kucoin_get_balance, kucoin_get_orders, STABLE_COINS
)
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from account.forms import InfoForm

from account.models import Info

# Create your views here.


@login_required
@require_http_methods(['GET'])
def coinex(request):
    if request.method == 'GET':
        coinex = get_coinex_client(request.user)
        balance_info = coinex.balance_info()
        balance = list()

        for key in balance_info.keys():
            if key in STABLE_COINS:
                continue

            d = {
                "name": key,
                "available": round(float(balance_info[key]['available']), 4),
                "last_price": get_market_last_price(request.user, f'{key}USDT'),
                "avg_buy_price": get_avg_buy_price(request.user, f'{key}USDT')
            }
            d['capital_involved'] = round(
                d['available'] * d['avg_buy_price'], 2
            )
            d['market_value'] = round(d['available'] * d['last_price'], 4)
            d['profit_loss'] = round(
                d['market_value'] - d['capital_involved'], 2
            )
            try:
                d['percent'] = round(
                    (d['profit_loss'] * 100) / d['capital_involved'], 2
                )
            except ZeroDivisionError:
                d['percent'] = 0

            d['text_color'] = "green" if d['profit_loss'] >= 0 else "red"
            balance.append(d)

        if "USDT" in balance_info.keys():
            balance.append({
                "name": "USDT",
                "available": round(float(balance_info["USDT"]['available']), 4),
                "last_price": 1.00,
                "avg_buy_price": 1.00,
                "capital_involved": round(float(balance_info["USDT"]['available']), 4),
                "market_value": round(float(balance_info["USDT"]['available']), 4),
                "profit_loss": round(float(balance_info["USDT"]['available']), 4),
                "text_color": "black",
                "percent": 0
            })

        if "USDC" in balance_info.keys():
            balance.append({
                "name": "USDC",
                "available": round(float(balance_info["USDC"]['available']), 4),
                "last_price": 1.00,
                "avg_buy_price": 1.00,
                "capital_involved": round(float(balance_info["USDC"]['available']), 4),
                "market_value": round(float(balance_info["USDC"]['available']), 4),
                "profit_loss": 0,
                "text_color": "black",
                "percent": 0
            })

        balance.sort(key=lambda x: x['market_value'], reverse=True)

        context = {
            "balance": balance,
            "logo": "https://mms.businesswire.com/media/20191220005131/en/764265/23/CoinEx_png.jpg"
        }
        return render(request, 'overview.html', context)


@login_required
@require_http_methods(['GET'])
def kucoin(request):
    client = get_kucoin_client(request.user)

    balance = kucoin_get_balance(client)
    orders = kucoin_get_orders(client)
    balance = kucoin_calculate(balance, orders, client)

    balance.sort(key=lambda x: x['market_value'], reverse=True)

    context = {
        "balance": balance,
        "logo": "https://assets.staticimg.com/cms/media/1lB3PkckFDyfxz6VudCEACBeRRBi6sQQ7DDjz0yWM.svg"
    }
    return render(request, 'overview.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def profile(request):
    info, _ = Info.objects.get_or_create(
        user=request.user,
        defaults={

        },
    )
    if request.method == "GET":
        form = InfoForm(instance=info)

    else:
        form = InfoForm(request.POST, instance=info)
        if form.is_valid():
            form.save()

    context = {"form": form}
    return render(request, "profile.html", context)
