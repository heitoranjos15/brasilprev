from django.db import models
from django.conf import settings


class Product(models.Model):

    name = models.TextField(max_length=250)
    width = models.IntegerField()
    depth = models.IntegerField()
    height = models.IntegerField()
    weight = models.FloatField()
    price = models.DecimalField(max_digits=6, decimal_places=2)


class Order(models.Model):
    client_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
