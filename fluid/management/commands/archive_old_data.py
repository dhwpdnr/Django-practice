from django.core.management.base import BaseCommand
from fluid.utils import archive_old_data


class Command(BaseCommand):
    """
    Example:
    python manage.py archive_old_data --days=30
    """

    help = "오래된 데이터를 아카이브 테이블로 이동"

    def add_arguments(self, parser):
        parser.add_argument(
            "--days", type=int, default=30, help="몇 일 이상된 데이터를 아카이브할지 설정 (기본값: 30일)"
        )

    def handle(self, *args, **kwargs):
        days = kwargs["days"]
        self.stdout.write(f"{days}일 이상된 데이터를 아카이브합니다...")
        archive_old_data(archive_days=days)
        self.stdout.write("아카이브 작업이 완료되었습니다.")
