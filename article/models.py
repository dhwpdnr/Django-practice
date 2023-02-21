from django.db import models
from django.contrib.auth.models import User
from common.models import CommonModel


class Article(CommonModel):

    """Article Model Definition"""

    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    writer = models.ForeignKey(
        "auth.User", related_name="articles", on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return self.title


class Comment(CommonModel):

    """Article Model Definition"""

    content = content = models.TextField(blank=True)
    writer = models.ForeignKey(
        "auth.User", related_name="comments", on_delete=models.SET_NULL, null=True
    )
    article = models.ForeignKey("article.Article", related_name="comments", on_delete=models.CASCADE)

    def __str__(self):
        return self.article
