from accounts.coinmarketcap import algoValue
from django import forms
from .models import Purchase, SellCoinExchange



class PurchaseForm(forms.ModelForm):
    price = algoValue()

    class Meta:
        model = Purchase
        fields = ['max_spend_usd', 'purchased_price', 'positions']
        labels = {"max_spend_usd": "Check your USD availability and enter the number of coins you wish to purchase",
                  'purchased_price': 'Enter the PRICE',
                  'positions': 'CURRENT PRICE/LIMIT PRICE'}
        widgets = {
            "purchased_price": forms.TextInput(attrs={"placeholder": "Enter the Price"})
        }


class SaleCoin(forms.ModelForm):
    current_price_market = algoValue()

    class Meta:
        model = SellCoinExchange
        fields = ['n_coin_sell', 'sell_price', 'positions']
        labels = {"n_coin_sell": "Enter the number of coins you wish to sell", 'sell_price': 'Enter the PRICE',
                  'positions': 'MARKET PRICE/LIMIT PRICE'}
        widgets = {
            "n_coin_sell": forms.TextInput(attrs={"placeholder": "Enter the number of coins you want to sell"})
        }
