from django.db import transaction
from rest_framework import serializers
from .models import TableMetadata, FieldMetadata, DynamicTableData


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


class DynamicTableDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DynamicTableData
        fields = ["id", "table", "data", "created_at", "updated_at"]

    def validate(self, attrs):
        table = attrs.get("table")
        data = attrs.get("data")

        # 필드 메타데이터 가져오기
        fields = FieldMetadata.objects.filter(table=table)

        for field in fields:
            field_name = field.name
            field_type = field.field_type
            if field_name not in data:
                raise serializers.ValidationError(f"필드 '{field_name}'는 필수입니다.")

            value = data[field_name]

            # 데이터 타입 검증 및 변환
            if field_type == "CharField":
                if field.max_length and len(value) > field.max_length:
                    raise serializers.ValidationError(
                        f"필드 '{field_name}'는 최대 {field.max_length}자를 초과할 수 없습니다."
                    )
                # CharField는 기본적으로 str로 처리
                if not isinstance(value, str):
                    data[field_name] = str(value)  # 변환

            elif field_type == "IntegerField":
                try:
                    data[field_name] = int(value)  # str을 int로 변환
                except ValueError:
                    raise serializers.ValidationError(f"필드 '{field_name}'는 정수여야 합니다.")

            elif field_type == "DecimalField":
                try:
                    data[field_name] = float(value)  # str을 float로 변환
                except ValueError:
                    raise serializers.ValidationError(f"필드 '{field_name}'는 숫자여야 합니다.")

            elif field_type == "TextField":
                if not isinstance(value, str):
                    data[field_name] = str(value)  # 변환

            # attrs를 업데이트된 data로 반환
        attrs["data"] = data
        return attrs
