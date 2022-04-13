from accounts.coinmarketcap import algoValue
from django import forms
from .models import Purchase, SellCoinExchange



class PurchaseForm(forms.ModelForm):
    price = algoValue()

    class Meta:
        model = Purchase
        fields = ['max_spend_usd']
        labels = {"max_spend_usd": "Enter the number of coins you wish to purchase"}
        
        
        
class SaleCoin(forms.ModelForm):
    current_price_market = algoValue()

    class Meta:
        model = SellCoinExchange
        fields = ['n_coin_sell']
        labels = {"n_coin_sell": "Enter the number of coins you wish to sell"}


