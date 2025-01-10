from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from .serializers import TableWithFieldsSerializer
from .serializers import DynamicTableDataSerializer
from .models import TableMetadata, DynamicTableData


class TableWithFieldsCreateView(generics.CreateAPIView):
    """테이블과 필드를 동시에 생성하는 API"""

    serializer_class = TableWithFieldsSerializer


class DynamicTableDataCreateView(generics.CreateAPIView):
    """동적 테이블 데이터를 생성하는 API"""

    queryset = DynamicTableData.objects.all()
    serializer_class = DynamicTableDataSerializer

    def create(self, request, *args, **kwargs):
        # 테이블 ID를 사용하여 테이블 확인
        table_id = kwargs.get("table_id")
        try:
            table = TableMetadata.objects.get(id=table_id)
        except TableMetadata.DoesNotExist:
            return Response(
                {"error": "테이블을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND
            )

        # 요청 데이터에 테이블 ID 추가
        data = request.data.copy()
        data = {"table": table.id, "data": data}

        # 데이터 생성
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
