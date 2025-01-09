from django.test import TestCase
from .models import TableMetadata, FieldMetadata
from django.urls import reverse


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
