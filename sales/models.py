from django.db import models
from django.db.models import Sum, F, FloatField

# Create your models here.
class ProductType(models.Model):
    product_type = models.CharField(max_length=1)
    cashback = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return self.product_type


class Product(models.Model):
    type = models.ForeignKey('ProductType', on_delete=models.CASCADE, blank=True, null= True)
    value = models.DecimalField(max_digits=5, decimal_places=2)
    qty = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.type)


class Cashback(models.Model):
    sold_at = models.DateTimeField()
    customer = models.ForeignKey('users.Customer', on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    products = models.ManyToManyField('Product', blank=True)
    cashback = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return str(self.customer) + " - " + str(self.sold_at)
