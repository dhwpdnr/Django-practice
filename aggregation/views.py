from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Book
from django.db.models import Avg, Sum, Max, F, FloatField


class AggregateTestAPI(APIView):
    def get(self, request):
        price_avg = Book.objects.all().aggregate(Avg("price"))
        total_price = Book.objects.all().aggregate(Sum("price"))
        max_price = Book.objects.all().aggregate(Max("price"))
        price_per_page = Book.objects.all().aggregate(
            price_per_page=Sum(F("price") / F("pages"), output_field=FloatField())
        )
        return Response(
            data={
                "price_avg": price_avg,
                "total_price": total_price,
                "max_price": max_price,
                "price_per_page": price_per_page,
            }
        )
