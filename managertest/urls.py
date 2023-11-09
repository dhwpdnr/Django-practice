from django.urls import path
from .apis import PersonActiveAPI, PersonAPI

urlpatterns = [
    path('person/active/list/', PersonActiveAPI.as_view()),
    path('person/list/', PersonAPI.as_view()),
]
