from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Book
from django.db.models import Avg


class AggregateTestAPI(APIView):
    def get(self, request):
        price_avg = Book.objects.all().aggregate(Avg("price"))

        return Response(data={})
