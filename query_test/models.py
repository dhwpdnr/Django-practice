from django.db import models


class Media(models.Model):
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    url = models.URLField()
