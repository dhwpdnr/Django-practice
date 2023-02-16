from rest_framework.pagination import PageNumberPagination
from collections import OrderedDict
from rest_framework.response import Response
from .models import *


# 페이지네이션 예시
class ProductsListAPIPageNumberPagination(PageNumberPagination):
    page_size = 10  # 페이지네이션 페이지 사이즈

    def get_paginated_response(self, data, total_count):

        try:
            previous_page_number = self.page.previous_page_number()
        except:
            previous_page_number = None

        try:
            next_page_number = self.page.next_page_number()
        except:
            next_page_number = None

        for i in data:
            category = Category.objects.filter(id=i["category"]).first()
            if category:
                i["category_name"] = category.name
            else:
                i["category_name"] = ""
        return Response(
            OrderedDict(
                [
                    ("data", data),
                    ("pageCnt", self.page.paginator.num_pages),
                    ("totalCnt", total_count),
                    ("curPage", self.page.number),
                    ("nextPage", next_page_number),
                    ("previousPage", previous_page_number),
                ]
            )
        )
