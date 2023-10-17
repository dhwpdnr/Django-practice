from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product, OrderLog
from django.db.models import F


class AnnotateTestAPI(APIView):
    def get(self, request):
        # row query
        data = OrderLog.objects.values('created', 'product__name', 'product__price')
        # use annotate, F in query
        data = OrderLog.objects.annotate(name=F('product__name'), price=F('product__price')).values('created', 'name',
                                                                                                    'price')

        return Response(data=data)
