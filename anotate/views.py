from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product, OrderLog
from django.db.models import F, Sum, Count
from django.db.models.functions import TruncDate
from django.db.models import Sum, F, DateField


class AnnotateTestAPI(APIView):
    def get(self, request):
        # row query
        data = OrderLog.objects.values("created", "product__name", "product__price")
        # use annotate, F in query
        data = OrderLog.objects.annotate(
            name=F("product__name"), price=F("product__price")
        ).values("created", "name", "price")
        daily_list = data.values("created").annotate(daily_total=Sum("product__price"))

        product_cnt_list = data.values("created", "name").annotate(
            product_cnt=Count("name")
        )

        return Response(
            data={
                "data": data,
                "daily_list": daily_list,
                "product_cnt_list": product_cnt_list,
            }
        )


class AggregateTestAPI(APIView):
    def get(self, request):
        order_logs = (
            OrderLog.objects.annotate(
                date=TruncDate("created", output_field=DateField())
            )
            .values("date")
            .annotate(total_price=Sum(F("product__price")))
            .order_by("date")
        )

        return Response(data=order_logs)
