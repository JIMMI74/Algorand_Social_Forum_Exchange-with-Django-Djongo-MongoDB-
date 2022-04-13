from accounts.coinmarketcap import algoValue
from django import forms
from .models import Purchase, SellCoinExchange



class PurchaseForm(forms.ModelForm):
    price = algoValue()

    class Meta:
        model = Purchase
        fields = ['max_spend_usd']
        
        
        
 class SaleCoin(forms.ModelForm):
    current_price_market = algoValue()

    class Meta:
        model = SellCoinExchange
        fields = ['n_coin_sell']

