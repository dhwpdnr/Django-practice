from datetime import timedelta
from django.utils.timezone import now
from django.db import transaction
from .models import DynamicTableData, ArchivedDynamicTableData


def archive_old_data(archive_days: int = 30):
    """
    오래된 데이터를 아카이브 테이블로 이동
    archive_days: 몇 일 이상된 데이터를 아카이브할지 설정 (기본값: 30일)
    """
    # 기준 날짜 계산
    cutoff_date = now() - timedelta(days=archive_days)

    # 데이터 조회
    old_data = DynamicTableData.objects.filter(created_at__lt=cutoff_date)

    if not old_data.exists():
        print("아카이브할 데이터가 없습니다.")
        return

    # 트랜잭션으로 데이터 이동
    with transaction.atomic():
        #  데이터를 삽입
        ArchivedDynamicTableData.objects.bulk_create(
            [
                ArchivedDynamicTableData(
                    table=record.table,
                    data=record.data,
                    created_at=record.created_at,
                    updated_at=record.updated_at,
                )
                for record in old_data
            ]
        )

        # 원본 데이터 삭제
        old_data.delete()

    print(f"{old_data.count()}개의 데이터를 아카이브했습니다.")
