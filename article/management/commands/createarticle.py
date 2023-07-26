from django.core.management import BaseCommand
from django.contrib.auth.models import User
from article.models import Article


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "name", type=str, help="article name", default="", nargs="?"
        )

    def handle(self, *args, **options):
        target_name = options.get("name")
        users = User.objects.all()

        if target_name:
            for user in users:
                for i in range(1, 6):
                    payload = {
                        "title": target_name,
                        "content": f"{i}번째 글 내용",
                        "writer": user
                    }
                    article = Article.objects.create(**payload)
                    print(f"{article.id} article created.")
        else:
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
