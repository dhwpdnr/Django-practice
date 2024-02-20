from rest_framework import generics, viewsets
from .seriializers import ArticleSerializer, ArticleCreateSerializer
from .models import Article
from drf_spectacular.utils import extend_schema, OpenApiExample


class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

    @extend_schema(
        request=ArticleCreateSerializer,
        responses={201: ArticleSerializer},
        examples=[
            OpenApiExample(
                "Create a new Article",
                summary="Create a new Article",
                value={
                    "title": "New Article",
                    "content": "New Article Content",
                },
            )
        ],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        request=ArticleCreateSerializer,
        responses={200: ArticleSerializer},
        examples=[
            OpenApiExample(
                "Update an Article",
                summary="Update an Article",
                value={
                    "title": "Updated Article",
                    "content": "Updated Article Content",
                },
            )
        ],
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        request=ArticleCreateSerializer,
        responses={200: ArticleSerializer},
        examples=[
            OpenApiExample(
                "Partial Update an Article",
                summary="Partial Update an Article",
                value={
                    "title": "Updated Article",
                },
            )
        ],
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
