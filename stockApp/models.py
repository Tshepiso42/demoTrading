from django.db import models
from django.contrib.auth.models import User
from .api_helper import stockSearch

class Stock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=20)
    name = models.CharField(max_length=20, null=True)
    shares_quantity = models.PositiveIntegerField(null=True)
    price = models.FloatField(null=True, blank=True)

    @property
    def get_total(self):
        return  round(self.price * self.shares_quantity, 2)

    def __str__(self):
        return self.name
    


class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=20)
    shares = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.symbol

class Cash(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_cash = models.FloatField(default=10000.00)

    def __str__(self):
        return "$" + str(round(self.user_cash))
        

