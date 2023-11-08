from django.urls import path
from .apis import PersonActiveAPI

urlpatterns = [
    path('person/active/list/', PersonActiveAPI.as_view()),
]
