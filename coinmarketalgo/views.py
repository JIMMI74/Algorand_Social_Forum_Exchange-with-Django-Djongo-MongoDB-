from django.shortcuts import render, redirect
from accounts.coinmarketcap import algoValue
from .forms import PurchaseForm, SaleCoin
from django.contrib import messages
from accounts.models import Profile
from django.http import HttpResponseBadRequest
from .models import PrincipalHome, SellCoinExchange




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
                    form.instance.commission_exchange = form.instance.sale_coin * form.instance.comm_exchange
                   
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




def HomePrincipalView(request):
    obj = PrincipalHome.objects.all()
    context = {'obj': obj}
    return render(request, 'coinmarketalgo/homepage.html', context)

