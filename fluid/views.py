from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from .serializers import TableWithFieldsSerializer
from .models import TableMetadata


class TableWithFieldsCreateView(generics.CreateAPIView):
    """테이블과 필드를 동시에 생성하는 API"""

    serializer_class = TableWithFieldsSerializer
