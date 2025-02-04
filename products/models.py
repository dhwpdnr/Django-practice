from django.db import models
from common.models import CommonModel


class Category(models.Model):
    """Category Model Definition"""

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Product(models.Model):
    """Product Model Definition"""

    name = models.CharField(max_length=200)
    price = models.IntegerField()
    category = models.ForeignKey(
        "products.Category",
        related_name="products",
        on_delete=models.SET_NULL,
        null=True,
    )

    def __str__(self):
        return self.name


class Option(CommonModel):
    """Option Model Definition"""

    name = models.CharField(max_length=30, default="", blank=True)
    product = models.ForeignKey(
        "products.Product", related_name="option", on_delete=models.CASCADE
    )
    price = models.PositiveIntegerField()
    stock = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Order(CommonModel):
    name = models.CharField(max_length=30)
    product = models.ManyToManyField("products.Product", related_name="order")
