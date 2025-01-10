from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from .models import TableMetadata, FieldMetadata, DynamicTableData


class TableWithFieldsTestCase(TestCase):
    def setUp(self):
        self.url = reverse("create-table-with-fields")

    def test_create_table_with_fields(self):
        """
        테이블과 필드를 동시에 생성하는 테스트
        """
        # 요청 데이터
        data = {
            "name": "세금 계산서",
            "description": "세금 관련 데이터를 관리하는 테이블",
            "fields": [
                {
                    "name": "상태",
                    "field_type": "CharField",
                    "max_length": 255,
                    "is_required": True,
                },
                {"name": "요청 번호", "field_type": "IntegerField", "is_required": True},
                {
                    "name": "송금액",
                    "field_type": "DecimalField",
                    "precision": 15,
                    "decimal_places": 2,
                    "is_required": True,
                },
            ],
        }

        # API 요청
        response = self.client.post(self.url, data, content_type="application/json")

        # 응답 확인
        self.assertEqual(response.status_code, 201)  # 201 Created
        response_data = response.json()
        self.assertIn("id", response_data)
        self.assertEqual(response_data["name"], data["name"])
        self.assertEqual(response_data["description"], data["description"])
        self.assertEqual(len(response_data["fields"]), 3)

        # 데이터베이스 확인
        table = TableMetadata.objects.get(name=data["name"])
        self.assertEqual(table.description, data["description"])
        self.assertEqual(table.fields.count(), 3)

        # 필드 확인
        field_names = [field["name"] for field in data["fields"]]
        for field in table.fields.all():
            self.assertIn(field.name, field_names)

        return table

    def test_create_table_with_invalid_field(self):
        """
        잘못된 필드 데이터로 인해 테이블 생성 실패 테스트
        """
        # 요청 데이터 (필드 타입이 잘못됨)
        data = {
            "name": "잘못된 테이블",
            "description": "테스트 설명",
            "fields": [
                {
                    "name": "잘못된 필드",
                    "field_type": "InvalidFieldType",  # 잘못된 타입
                    "is_required": True,
                }
            ],
        }

        # API 요청
        response = self.client.post(self.url, data, content_type="application/json")

        # 응답 확인
        self.assertEqual(response.status_code, 400)  # 400 Bad Request
        response_data = response.json()
        self.assertIn("fields", response_data)

        # 데이터베이스 확인 (테이블이 생성되지 않았는지 확인)
        self.assertFalse(TableMetadata.objects.filter(name=data["name"]).exists())

    def test_partial_failure_rolls_back(self):
        """
        필드 생성 중 오류가 발생했을 때, 테이블 생성도 롤백되는지 테스트
        """
        data = {
            "name": "테이블 롤백 테스트",
            "description": "테이블 생성 중 오류 발생 테스트",
            "fields": [
                {
                    "name": "정상 필드",
                    "field_type": "CharField",
                    "max_length": 255,
                    "is_required": True,
                },
                {
                    "name": "오류 필드",
                    "field_type": "InvalidFieldType",  # 잘못된 타입
                    "is_required": True,
                },
            ],
        }

        # API 요청
        response = self.client.post(self.url, data, content_type="application/json")

        # 응답 확인
        self.assertEqual(response.status_code, 400)  # 400 Bad Request

        # 데이터베이스 확인 (테이블 및 필드가 생성되지 않았는지 확인)
        self.assertFalse(TableMetadata.objects.filter(name=data["name"]).exists())
        self.assertFalse(FieldMetadata.objects.filter(name="정상 필드").exists())

    def test_create_dynamic_table_data_success(self):
        table = self.test_create_table_with_fields()

        data = {"상태": "처리 완료", "요청 번호": 12345, "송금액": 1500.50}

        response = self.client.post(
            f"/fluid/table/{table.id}/data", data, format="json"
        )

        # 응답 확인
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertEqual(response.data["table"], table.id)
        self.assertEqual(response.json()["data"], data)

        # 데이터베이스 확인
        self.assertEqual(DynamicTableData.objects.count(), 1)
        saved_data = DynamicTableData.objects.first()
        self.assertEqual(saved_data.data["상태"], data["상태"])
        self.assertEqual(saved_data.data["요청 번호"], data["요청 번호"])
        self.assertEqual(float(saved_data.data["송금액"]), data["송금액"])

    def test_create_dynamic_table_data_missing_field(self):
        """필수 필드가 누락되었을 때의 실패 테스트"""
        table = self.test_create_table_with_fields()
        data = {
            "상태": "처리 완료",
            # "요청 번호": 12345,  # 누락
            "송금액": 1500.50,
        }

        response = self.client.post(
            f"/fluid/table/{table.id}/data", data, format="json"
        )

        # 응답 확인
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print(response.json())
        self.assertIn("non_field_errors", response.data)
        self.assertIn("필드 '요청 번호'는 필수입니다.", response.data["non_field_errors"])

        # 데이터베이스 확인
        self.assertEqual(DynamicTableData.objects.count(), 0)

    def test_create_dynamic_table_data_invalid_table(self):
        """
        존재하지 않는 테이블에 데이터를 생성하려는 실패 테스트
        """
        invalid_url = "/fluid/table/9999/data"  # 존재하지 않는 테이블 ID
        data = {"상태": "처리 완료", "요청 번호": 12345, "송금액": 1500.50}

        response = self.client.post(invalid_url, data, format="json")

        # 응답 확인
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "테이블을 찾을 수 없습니다.")

        # 데이터베이스 확인
        self.assertEqual(DynamicTableData.objects.count(), 0)
