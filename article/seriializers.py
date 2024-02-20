from rest_framework import serializers
from .models import Article


class ArticleSerializer(serializers.Serializer):
    class Meta:
        model = Article
        fields = "__all__"


class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ["title", "content"]
