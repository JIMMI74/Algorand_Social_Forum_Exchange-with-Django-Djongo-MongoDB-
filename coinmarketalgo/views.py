from django.shortcuts import render, redirect, get_object_or_404
from accounts.coinmarketcap import algoValue
from .forms import PurchaseForm, SaleCoin
from django.contrib import messages
from accounts.models import Profile
from django.http import HttpResponseBadRequest
from .models import PrincipalHome, SellCoinExchange, Purchase
from django.db.models import Avg, Max, Min, Sum
from django.contrib.auth.models import User
from ordertransaction.models import Order, Transaction
import math



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
                    print('Commission = ', str(form.instance.commission_exchange_buy) + ", USD_wallet net commission = " + str(buyer.USD_wallet))

                    form.save()
                    buyer.save()
                    messages.success(request, f"Your purchase order has been sent to the exchange and processed,"
                                     f" n ALGO you buy = {buyer.ALGO_Wallet} ALGO, net of commission of {form.instance.commission_exchange_buy} USD")
                    messages.success(request, f"Total Coin Purchased = {buyer.ALGO_Wallet} ALGO")
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
    ctv_sum_purchase = 0
    total_bought_coin_purchase = 0
    ctv_sum_transaction = 0
    total_bought_coin_transaction = 0
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
                    coin_bought_purchase = Purchase.objects.filter(profile=form.instance.profile)
                    coin_bought_transaction = Transaction.objects.filter(call_id=request.user)
                    print(coin_bought_purchase)
                    print(coin_bought_transaction)
                    for orders in coin_bought_purchase:
                        ctv_sum_purchase += orders.purchased_price * orders.purchased_coin
                        print(ctv_sum_purchase)
                        total_bought_coin_purchase += orders.purchased_coin
                    try:
                        avg_price_orders_seller = ctv_sum_purchase / total_bought_coin_purchase     # 1)  average price Purchase
                    except ZeroDivisionError:
                        avg_price_orders_seller = 0

                    print('Average Price Orders Seller =', avg_price_orders_seller)
                    avg_orders = avg_price_orders_seller

                    for transactions in coin_bought_transaction:
                        ctv_sum_transaction += transactions.price * transactions.quantity
                        print(ctv_sum_transaction)
                        total_bought_coin_transaction += transactions.quantity
                    try:
                        avg_price_transactions_seller = ctv_sum_transaction / total_bought_coin_transaction    #) 2 avergare price Transaction
                    except ZeroDivisionError:
                        avg_price_transactions_seller = 0
                    print('Average Price Seller =', avg_price_transactions_seller)
                    avg_transactions = avg_price_transactions_seller

                    total_avg_price_seller = (avg_transactions + avg_orders) / 2          # 3) arithmetic mean of the two averages
                    print('Total Average Loading Price =', total_avg_price_seller)

                    
                    ctv_n_coin_sell_loading_price = (form.instance.n_coin_sell * total_avg_price_seller)     # 4) loading price of coins for sale
                    print('Ctv nCoin in Sell * Avg Loading Price', str(ctv_n_coin_sell_loading_price) + "= (nCoin Sell) =" + str(form.instance.n_coin_sell) + " * (Average Price to charge)" + str(total_avg_price_seller))

                    gain_loss_exchange = form.instance.sale_coin - ctv_n_coin_sell_loading_price
                    print('Gain/Loss', str(gain_loss_exchange) + "= CTV nCoin Sell" + str(form.instance.sale_coin) + " - nCoin in Sell =" + str(form.instance.n_coin_sell) + " * Average Loading Price =" + str(total_avg_price_seller))

                    form.instance.net_profit = gain_loss_exchange - form.instance.commission_exchange
                    print('Net Profit', str(form.instance.net_profit) + "= Gain Loss " + str(gain_loss_exchange) + "- Commission Exchange =" + str(form.instance.commission_exchange))

                    seller.ALGO_Wallet -= form.instance.n_coin_sell
                    seller.USD_wallet += form.instance.sale_coin - form.instance.commission_exchange
                    seller.profit += form.instance.net_profit
                    print('USD Wallet', str(seller.USD_wallet) + '+ Sale Coin ' + str(form.instance.sale_coin) + ' - Commission Exchange =', str(form.instance.commission_exchange))

                    form.save()
                    seller.save()
                    messages.success(request,
                                     f"Your sales order has been sent to the exchange and processed,"
                                     f" sales value = {seller.USD_wallet} USD, net of commission. "
                                     f"Your Gain/Loss has been of {gain_loss_exchange}USD")
                    messages.success(request,f'Now your net profit is {form.instance.net_profit}USD')

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
    try:
        avg_price = sum_ctv / total_coin_purchase
                                                            
    except ZeroDivisionError:
        avg_price = 0
    print(avg_price)

    sum_ctv_tr = 0
    total_coin_quantity = 0

    for transaction in transactions:
        sum_ctv_tr += (transaction.price * transaction.quantity)
        total_coin_quantity += transaction.quantity

    print(sum_ctv_tr)
    print(total_coin_quantity)
    print(profile)
    try:
        avg_price_tr = sum_ctv_tr / total_coin_quantity
    except ZeroDivisionError:
        avg_price_tr = 0
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

