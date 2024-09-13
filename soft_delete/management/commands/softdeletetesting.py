from django.core.management.base import BaseCommand
from soft_delete.models import SoftDelete


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Soft Delete 테스트
        # 1. SoftDelete 객체 생성
        instance = SoftDelete.objects.create(name="test")
        self.stdout.write(f"instance name : {instance.name}")
        # 2. 객체 삭제
        instance.delete()
        self.stdout.write("instance soft delete")

        # 3. 삭제된 객체 조회
        self.stdout.write(f"SoftDelete.objects.all() : {SoftDelete.objects.all()}")

        # 4. 중복 생성
        try:
            instance = SoftDelete.objects.create(name="test")
        except Exception as e:
            self.stdout.write(f"instance create error : {e}")
