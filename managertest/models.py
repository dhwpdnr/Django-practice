from django.db import models


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True)


class Article(models.Model):
    """Article model Definition"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    active = models.BooleanField(default=True)
    active_objects = ActiveManager()

    def __str__(self):
        return self.name


class Magazine(models.Model):
    """Magazine Model Definition"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    active = models.BooleanField(default=True)
    active_objects = ActiveManager()

    def __str__(self):
        return self.name
