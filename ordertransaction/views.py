from django.shortcuts import render, redirect, HttpResponseRedirect
from .forms import OrderForm
from accounts.models import Profile
from accounts.coinmarketcap import algoValue
from .models import Order, Transaction
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required




@login_required
def placeOrders(request):
    price_traded_on_exchange = algoValue()
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.profile = Profile.objects.get(user=request.user)
            decision = form.instance.position
            if form.instance.price < 0 or form.instance.quantity_max_insert < 0:
                messages.warning(request, 'Add money !')
                return redirect('/buy_sell_dex/')
            if decision == 'BUY' and (form.instance.price * form.instance.quantity_max_insert) > form.instance.profile.\
                    USD_wallet:
                messages.warning(request, 'you do not have enough funds to complete the operation!')
                return redirect('/buy_sell_dex/')
            if decision == 'SELL' and form.instance.quantity_max_insert > form.instance.profile.ALGO_Wallet:
                messages.warning(request, 'You cannot sell more Coin than you have!')
                return redirect('/buy_sell_dex/')
            form.save()
            messages.success(request, 'Your Order has been created successfully')

            orders = Order.objects.latest('datetime')
            print(str(orders.profile) + "+" + str(orders.quantity_max_insert))
            open_buyers = Order.objects.filter(position='BUY', status='open').order_by('-price')
            open_sellers = Order.objects.filter(position='SELL', status='open').order_by('price')

            if orders.position == 'BUY' and open_sellers.count() > 0:
                for sell in open_sellers:
                    if sell.price <= orders.price:
                        put_trader = sell.profile
                        call_trader = orders.profile
                        if sell.quantity_max_insert <= orders.quantity_max_insert:
                            call_trader.USD_wallet -= (sell.price * sell.quantity_max_insert)
                            call_trader.ALGO_Wallet += sell.quantity_max_insert
                            put_trader.USD_wallet += (sell.price * sell.quantity_max_insert)
                            put_trader.ALGO_Wallet -= sell.quantity_max_insert
                            orders.quantity_max_insert -= sell.quantity_max_insert
                            if orders.quantity_max_insert == 0.0:
                                orders.status = 'closed'

                            Transaction.objects.create(call=call_trader.user, put=put_trader.user,
                                                       price=sell.price, quantity=sell.quantity_max_insert)
                            put_trader.profit += (sell.price * sell.quantity_max_insert)
                            call_trader.profit -= (sell.price * sell.quantity_max_insert)

                            sell.status = 'closed'
                            sell.quantity_max_insert = 0.0

                        else:

                            call_trader.USD_wallet -= (sell.price * orders.quantity_max_insert)
                            call_trader.ALGO_Wallet += orders.quantity_max_insert
                            put_trader.USD_wallet += (sell.price * orders.quantity_max_insert)
                            put_trader.ALGO_Wallet -= orders.quantity_max_insert

                            sell.quantity_max_insert -= orders.quantity_max_insert

                            Transaction.objects.create(call=orders.profile.user, put=put_trader.user,
                                                       quantity=orders.quantity_max_insert, price=sell.price)

                            call_trader.profit -= (sell.price * orders.quantity_max_insert)
                            put_trader.profit += (sell.price * orders.quantity_max_insert)

                            orders.status = 'closed'
                            orders.quantity = 0.0

                        put_trader.save()
                        call_trader.save()
                        orders.save()
                        sell.save()

            if orders.position == 'SELL' and open_buyers.count() > 0:
                for buy in open_buyers:
                    if buy.price >= orders.price:
                        call_trader = buy.profile
                        put_trader = orders.profile

                        if buy.quantity_max_insert <= orders.quantity_max_insert:
                            call_trader.USD_wallet -= (buy.price * buy.quantity_max_insert)
                            call_trader.ALGO_Wallet += buy.quantity_max_insert
                            put_trader.USD_wallet += (buy.price * buy.quantity_max_insert)
                            put_trader.ALGO_Wallet -= buy.quantity_max_insert
                            orders.quantity_max_insert -= buy.quantity_max_insert
                            if orders.quantity_max_insert == 0.0:
                                orders.status = 'closed'

                            Transaction.objects.create(call=call_trader.user, put=put_trader.user,
                                                       quantity=buy.quantity_max_insert, price=buy.price)
                            call_trader.profit -= (buy.price * buy.quantity_max_insert)
                            put_trader.profit += (buy.price * buy.quantity_max_insert)
                            buy.status = 'closed'
                            buy.quantity_max_insert = 0.0
                        else:
                            call_trader.USD_wallet -= (buy.price * orders.quantity_max_insert)
                            call_trader.ALGO_Wallet += orders.quantity_max_insert
                            put_trader.USD_wallet += (buy.price * orders.quantity_max_insert)
                            put_trader.ALGO_Wallet -= orders.quantity_max_insert
                            buy.quantity_max_insert -= orders.quantity_max_insert

                            Transaction.objects.create(call=call_trader.user, put=put_trader.user,
                                                       quantity=orders.quantity_max_insert, price=buy.price)

                            call_trader.profit -= (orders.price * orders.quantity_max_insert)
                            put_trader.profit += (orders.price * orders.quantity_max_insert)

                            # current order is done
                            orders.status = 'closed'
                            orders.quantity = 0.0

                        put_trader.save()
                        call_trader.save()
                        buy.save()
                        orders.save()
                        messages.success(request, ('great, your transaction was successful'))

            return redirect("match_orders")
    else:
        form = OrderForm()

    return render(request, "ordertransaction/match_orders.html", {'form': form, 'price_traded_on_exchange': price_traded_on_exchange})


@login_required
def activeOrders(request):
    response = []
    ord_active = Order.objects.filter(status='open')
    for data in ord_active:
        response.append(
            {
                'price': data.price,
                'position': data.position,
                "quantity_max_insert": data.quantity_max_insert,
                "datetime": data.datetime,
            }
        )
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    user_current = Profile.objects.filter(user=request.user)[0]
    user_current.ips.append(ip)
    user_current.save(update_fields=['ips'])

    return JsonResponse(response, safe=False)



def gain_loss(request):
    response = []
    profiles = Profile.objects.all()
    for profile in profiles:
        response.append(
            {
                "user": profile.user.username,
                "ALGO_Wallet": profile.ALGO_Wallet,
                "USD_wallet": profile.USD_wallet,
                "profit/losses": profile.profit,
            }
        )
    return JsonResponse(response, safe=False)

@login_required
def order_status_book_view(request):  # with view
    orders = Order.objects.all().order_by('-datetime')
    order_paginator = Paginator(orders, 10)
    page_num = request.GET.get("page")
    page = order_paginator.get_page(page_num)
    context = {'orders': orders, 'count': order_paginator.count, 'page': page}
    return render(request, 'ordertransaction/match_status.html', context)


def transaction_user(request):  # with json
    response = []
    operations = Transaction.objects.filter(Q(call=request.user) | Q(put=request.user))
    for transdone in operations:
        response.append(
            {

                "quantity": transdone.quantity,
                "price": transdone.price,
                "datetime": transdone.datetime,
                "buyer": transdone.call.username,
                "seller": transdone.put.username,
            }
        )

    return JsonResponse(response, safe=False)
