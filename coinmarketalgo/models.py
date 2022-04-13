from django.db import models
from djongo.models.fields import ObjectIdField
from accounts.models import Profile


class Purchase(models.Model):
    _id = ObjectIdField()
    max_spend_usd = models.FloatField(default=0)
    purchased_price = models.FloatField(default=0)
    datetime = models.DateTimeField(auto_now_add=True)
    purchased_coin = models.FloatField(default=0)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile')
    comm_exchange_buy = models.FloatField(default=1 / 100)
 


class SellCoinExchange(models.Model):
    _id = ObjectIdField()    
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    sale_coin = models.FloatField(default=0)
    sell_price = models.FloatField(default=0)
    n_coin_sell = models.FloatField(default=0)
    datetime = models.DateTimeField(auto_now_add=True)
    comm_exchange = models.FloatField(default=0.5 / 100)
    
    
    
class PrincipalHome(models.Model):
    title_principal = models.CharField(max_length=150)
    sub_title = models.CharField(max_length=150, blank=True, null=True)
    image = models.ImageField(upload_to="pics/%y/%m/%d/")
    action_name = models.CharField(max_length=50)
    link = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title_principal
