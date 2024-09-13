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
    name = models.CharField(max_length=255, unique=True)

    objects = SoftDeleteManager()
    all_objects = AllObjectsManager()

    def delete(self, using=None, keep_parents=False):
        self.deleted = True
        self.save()

    def hard_delete(self, using=None, keep_parents=False):
        super(SoftDelete, self).delete(using, keep_parents)
