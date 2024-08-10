from rest_framework import generics
from rest_framework.response import Response
from products.models import Product, Category


class QueryTestAPI(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        # 전체 조회
        products_query = Product.objects.all()
        print(str(products_query.query))

        # join 사용
        products_select_related = Product.objects.select_related("category").all()
        print(str(products_select_related.query))

        return Response({"message": "Query Test API"})
