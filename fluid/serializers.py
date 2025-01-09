from django.db import transaction
from rest_framework import serializers
from .models import TableMetadata, FieldMetadata


class FieldMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldMetadata
        fields = [
            "id",
            "name",
            "field_type",
            "max_length",
            "decimal_places",
            "precision",
            "is_required",
            "default_value",
        ]


class TableWithFieldsSerializer(serializers.ModelSerializer):
    fields = FieldMetadataSerializer(many=True)  # 필드 리스트를 포함

    class Meta:
        model = TableMetadata
        fields = ["id", "name", "description", "fields"]

    def create(self, validated_data):
        with transaction.atomic():
            # 테이블 데이터와 필드 데이터를 분리
            fields_data = validated_data.pop("fields")
            table = TableMetadata.objects.create(**validated_data)

            # 필드 생성
            for field_data in fields_data:
                FieldMetadata.objects.create(table=table, **field_data)

            return table
