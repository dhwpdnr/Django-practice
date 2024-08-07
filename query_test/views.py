from rest_framework import generics
from rest_framework.response import Response
from products.models import Product, Category


class QueryTestAPI(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        return Response({"message": "Query Test API"})
