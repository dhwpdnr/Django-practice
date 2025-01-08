from django.db import models, transaction
from utils import send_webhook


class WebhookTestModel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # 데이터를 저장하고 웹훅 호출
        try:
            # 트랜잭션 시작
            with transaction.atomic():
                # 데이터 저장
                super().save(*args, **kwargs)

                # 웹훅 호출 로직
                payload = {
                    "name": self.name,
                    "description": self.description,
                }

                # 웹훅 URL
                url = "https://webhook.site/7b2e7f0e-8c9e-4f9e-9a7a-6b7a4e7c6d3e"

                # 웹훅 호출
                response = send_webhook(url, payload)

                # 웹훅 요청 실패 시 예외 발생
                if not response or response.status_code != 200:
                    raise Exception(
                        f"Webhook failed with status: {response.status_code}"
                    )
        except Exception as e:
            # 실패 로그 출력
            print(f"Transaction rolled back due to: {e}")
            raise e
