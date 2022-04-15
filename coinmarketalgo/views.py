from django.shortcuts import render, redirect, get_object_or_404
from accounts.coinmarketcap import algoValue
from .forms import PurchaseForm, SaleCoin
from django.contrib import messages
from accounts.models import Profile
from django.http import HttpResponseBadRequest
from .models import PrincipalHome, SellCoinExchange, Purchase
from django.db.models import Sum
from django.contrib.auth.models import User
from ordertransaction.models import Order, Transaction




def buyalgomkt(request):
    new_price = algoValue()
    if request.method == "POST":
        form = PurchaseForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.profile = Profile.objects.get(user=request.user)
            form.instance.purchased_price = new_price
            if (
                form.instance.profile.USD_wallet > 0
                and form.instance.max_spend_usd < form.instance.profile.USD_wallet
            ):
                if form.instance.max_spend_usd > 0:
                    form.instance.purchased_coin = form.instance.max_spend_usd / new_price
                    form.instance.commission_exchange_buy = form.instance.purchased_coin * form.instance.comm_exchange_buy
                    buyer = Profile.objects.get(user=request.user)
                    buyer.ALGO_Wallet += form.instance.purchased_coin
                    buyer.USD_wallet -= form.instance.max_spend_usd - form.instance.commission_exchange_buy
                    print(str(form.instance.commission_exchange_buy) + "+" + str(buyer.USD_wallet))

                    form.save()
                    buyer.save()
                    messages.success(request, f"Your purchase order has been sent to the exchange and processed,"
                                     f" n ALGO you buy = {buyer.ALGO_Wallet} ALGO, net of commission. ")
                else:
                    messages.warning(request, "You do not have enough money or import is not correct!")
                return redirect("purchase")
            else:
                messages.warning(request, "You do not have enough money!")
            return redirect("purchase")
        else:
            return HttpResponseBadRequest()

    else:
        form = PurchaseForm()

    return render(
        request, "coinmarketalgo/purchase.html", {"form": form, "new_price": new_price}
    )






def sellcoinexchange(request):
    current_price_market = algoValue()
    if request.method == "POST":
        form = SaleCoin(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.profile = Profile.objects.get(user=request.user)
            form.instance.sell_price = current_price_market
            if (
                form.instance.profile.ALGO_Wallet > 0
                and form.instance.n_coin_sell <= form.instance.profile.ALGO_Wallet
            ):
                if form.instance.n_coin_sell > 0:
                    form.instance.sale_coin = form.instance.n_coin_sell * current_price_market
                    form.instance.commission_exchange = form.instance.sale_coin * form.instance.comm_exchange_sell
                   
                    seller = Profile.objects.get(user=request.user)
                    seller.ALGO_Wallet -= form.instance.n_coin_sell
                    seller.USD_wallet += form.instance.sale_coin - form.instance.commission_exchange
                    print(str(form.instance.commission_exchange) + "+" + str(seller.USD_wallet))
                    form.save()
                    seller.save()
                    messages.success(request,
                                     f"Your sales order has been sent to the exchange and processed,"
                                     f" sales value = {seller.USD_wallet} USD, net of commission. ")

                else:
                    messages.warning(request, "Attention enter a correct value please! ")
                return redirect("sell_exchange")

            else:
                messages.warning(request, "You do not have enough coins!")
            return redirect("sell_exchange")

        else:
            return HttpResponseBadRequest()

    else:
        form = SaleCoin()

    return render(
        request, "coinmarketalgo/sell_exchange.html", {"form": form, "current_price_market": current_price_market}
    )


def list_price_average(request, username):
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)
    purchases = Purchase.objects.filter(profile=profile).order_by('-datetime')
    orders = Order.objects.filter(profile=profile).order_by('-datetime')
    transactions = Transaction.objects.filter(call=request.user).order_by('-datetime')
    sum_ctv = 0
    total_coin_purchase = 0

    for purchase in purchases:
       sum_ctv += purchase.purchased_price * purchase.purchased_coin
       total_coin_purchase += purchase.purchased_coin

    print(sum_ctv)
    print(len(purchases))
    print(total_coin_purchase)
    avg_price = sum_ctv / total_coin_purchase
    print(avg_price)

    sum_ctv_tr = 0
    total_coin_quantity = 0

    for transaction in transactions:
        sum_ctv_tr += (transaction.price * transaction.quantity)
        total_coin_quantity += transaction.quantity

    print(sum_ctv_tr)
    print(total_coin_quantity)
    print(profile)
    avg_price_tr = sum_ctv_tr / total_coin_quantity
    print(avg_price_tr)

    total_average_price_coin = (avg_price + avg_price_tr) / 2
    print(total_average_price_coin)

    context = {'user': user, 'profile': profile, 'purchases': purchases,
               'orders': orders, 'transactions': transactions, 'avg_price': avg_price, 'avg_price_tr': avg_price_tr,
               'total_average_price_coin': total_average_price_coin}
    return render(request, 'coinmarketalgo/total_average_price_coin.html', context)
    


def HomePrincipalView(request):
    obj = PrincipalHome.objects.all()
    context = {'obj': obj}
    return render(request, 'coinmarketalgo/homepage.html', context)

