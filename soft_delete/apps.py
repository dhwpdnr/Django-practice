from django.apps import AppConfig


class SoftDeleteConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "soft_delete"
