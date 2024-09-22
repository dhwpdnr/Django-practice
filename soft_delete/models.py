from django.db import models
from django.utils import timezone


class SoftDeleteQuerySet(models.QuerySet):
    def delete(self):
        return super(SoftDeleteQuerySet, self).update(
            deleted=True, deleted_at=timezone.now()
        )

    def hard_delete(self):
        return super(SoftDeleteQuerySet, self).delete()


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).filter(deleted=False)


class AllObjectsManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db)


class SoftDelete(models.Model):
    deleted = models.BooleanField(default=False)  # 삭제 여부를 나타내는 필드
    name = models.CharField(max_length=255)

    objects = SoftDeleteManager()
    all_objects = AllObjectsManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name"],  # 'name' 컬럼에 대해 unique 제약을 걸되,
                condition=models.Q(deleted=False),  # deleted가 False일 때만 적용
                name="unique_name_partial_index",  # 인덱스의 이름을 지정
            )
        ]

    def delete(self, using=None, keep_parents=False):
        self.deleted = True
        self.save()

    def hard_delete(self, using=None, keep_parents=False):
        super(SoftDelete, self).delete(using, keep_parents)


class Foo(models.Model):
    deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    name = models.CharField(max_length=255)

    objects = SoftDeleteManager()
    all_objects = AllObjectsManager()

    def delete(self, using=None, keep_parents=False):
        self.deleted = True
        Bar.objects.filter(foo=self).delete()
        self.save()


class Bar(models.Model):
    deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    name = models.CharField(max_length=255)
    foo = models.ForeignKey(Foo, on_delete=models.CASCADE)

    objects = SoftDeleteManager()
    all_objects = AllObjectsManager()
