from django.core.management import BaseCommand
from django.contrib.auth.models import User
from article.models import Article


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("title", type)

    def handle(self, *args, **options):
        users = User.objects.all()
        for user in users:
            for i in range(1, 6):
                payload = {
                    "title": f"{user.username}의 {i}번째 글",
                    "content": f"{i}번째 글 내용",
                    "writer": user
                }
                article = Article.objects.create(**payload)
                print(f"{article.id} article created.")

        self.stdout.write(self.style.SUCCESS('Successfully created Article'))
