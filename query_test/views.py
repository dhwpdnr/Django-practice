from rest_framework import generics
from rest_framework.response import Response
from django.db import models
from django.db.models import Subquery, OuterRef, Prefetch
from products.models import Product, Category
from .models import Media


class QueryTestAPI(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        # 전체 조회
        products_query = Product.objects.all()
        print(str(products_query.query))

        # join 사용
        products_select_related = Product.objects.select_related("category").all()
        print(str(products_select_related.query))

        # 아래 구문은 쿼리를 총 2번 실행합니다.
        products = Product.objects.all()  # 아직 실행 X
        firs_product = products[0]  # 실행 O
        products_list = list(products)  # 실행 O

        # 아래는 쿼리를 2번 실행
        product = Product.objects.prefetch_related("media_set").get(
            content="test"
        )  # 실행 O
        media = product.meida_set.first()  # 실행 O
        # 전체를 가져 왔지만 first()를 사용했기 때문에 쿼리가 1번 더 실행됨

        # annotate 와 subquery 를 사용한 쿼리 최적화
        thumbnail = Subquery(
            Media.objects.filter(product_id=OuterRef("pk")).values("url")[:1],
            output_field=models.URLField(),
        )
        product = (
            Product.objects.annotate(thumbnail=thumbnail)
            .prefetch_related("media_set")
            .get(content="test")
        )

        # prefetch_related 와 Prefetch 를 사용한 쿼리 최적화
        product = Product.objects.prefetch_related(Prefetch("")).get(content="test")

        return Response({"message": "Query Test API"})
