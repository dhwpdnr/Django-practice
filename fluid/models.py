from django.db import models


class TableMetadata(models.Model):
    """사용자 정의 테이블을 메타데이터로 관리하기 위한 모델."""

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class FieldMetadata(models.Model):
    """사용자 정의 테이블에 포함된 필드의 메타데이터를 관리하기 위한 모델."""

    FIELD_TYPE_CHOICES = [
        ("CharField", "문자열 (CharField)"),
        ("IntegerField", "정수 (IntegerField)"),
        ("DecimalField", "소수 (DecimalField)"),
        ("TextField", "텍스트 (TextField)"),
    ]

    table = models.ForeignKey(
        TableMetadata, on_delete=models.CASCADE, related_name="fields"
    )
    name = models.CharField(max_length=255)  # 필드 이름
    field_type = models.CharField(max_length=50, choices=FIELD_TYPE_CHOICES)  # 필드 타입
    max_length = models.IntegerField(
        blank=True, null=True
    )  # CharField나 TextField의 최대 길이
    decimal_places = models.IntegerField(
        blank=True, null=True
    )  # DecimalField에서 소수점 자리수
    precision = models.IntegerField(blank=True, null=True)  # DecimalField의 정밀도
    is_required = models.BooleanField(default=False)  # 필드가 필수인지 여부
    default_value = models.CharField(
        max_length=255, blank=True, null=True
    )  # 기본값 (선택사항)

    def __str__(self):
        return f"{self.table.name} - {self.name}"


class DynamicTableData(models.Model):
    table = models.ForeignKey(
        TableMetadata, on_delete=models.CASCADE, related_name="data"
    )
    data = models.JSONField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
