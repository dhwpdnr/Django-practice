from django.urls import path
from .apis import ArticleViewSet

urlpatterns = [
    path(
        "article/",
        ArticleViewSet.as_view(
            {
                "post": "create",
            }
        ),
    ),
    path(
        "article/<int:pk>/",
        ArticleViewSet.as_view(
            {
                "put": "update",
                "patch": "partial_update",
            }
        ),
    ),
]
