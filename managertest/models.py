from django.db import models


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True)


class AbstractBase(models.Model):
    active_objects = ActiveManager()
    objects = models.Manager()

    class Meta:
        abstract = True


class Article(AbstractBase):
    """Article model Definition"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Magazine(AbstractBase):
    """Magazine Model Definition"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class PersonManager(models.Manager):
    def author(self):
        return self.get_queryset().filter(role="A")

    def editor(self):
        return self.get_queryset().filter(role="E")


class ActivePersonManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True)

    def author(self):
        return self.get_queryset().filter(role="A")

    def editor(self):
        return self.get_queryset().filter(role="E")


class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=1, choices=[("A", ("Author")), ("E", ("Editor"))])
    active = models.BooleanField(default=True)
    people = PersonManager()
    active_people = ActivePersonManager()
