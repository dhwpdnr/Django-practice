from rest_framework import generics
from .serializers import *
from .pagination import *


class ProductsListAPI(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductsListAPIPageNumberPagination

    def get_paginated_response(self, data, total_count):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data, total_count)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        total_count = queryset.count()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data, total_count)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
