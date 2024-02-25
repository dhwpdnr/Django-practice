from rest_framework import generics, viewsets
from .seriializers import ArticleSerializer, ArticleCreateSerializer
from .models import Article
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter
from drf_spectacular.types import OpenApiTypes


class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

    @extend_schema(
        tags=["테스트"],
        summary="method레벨 데코레이터도 가능",
        parameters=[
            OpenApiParameter(
                name="a_param", description="QueryParam1 입니다.", required=False, type=str
            ),
            OpenApiParameter(
                name="date_param",
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.QUERY,
                description="Filter by release date",
                examples=[
                    OpenApiExample(
                        "이것은 Query Parameter Example입니다.",
                        summary="short optional summary",
                        description="longer description",
                        value="1993-08-23",
                    ),
                ],
            ),
        ],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        request=ArticleCreateSerializer,
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
