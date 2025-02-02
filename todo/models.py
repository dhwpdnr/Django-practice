from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=255)


class Comment(models.Model):
    task = models.ForeignKey(Task, related_name="comments", on_delete=models.CASCADE)
    content = models.TextField()
