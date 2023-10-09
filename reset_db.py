import os, sys
import shutil
from config import settings

reset_target_list = []

reset_migrations_list = [os.path.join(i, "migrations") for i in settings.CUSTOM_APPS]


def reset_dir(dir_path):
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
    os.makedirs(dir_path)


def reset_data():
    for reset_target in reset_target_list:
        reset_dir(reset_target)


def reset_migrate(reset_dir):
    for item in os.listdir(reset_dir):
        if item != "__init__.py":
            target_path = os.path.join(reset_dir, item)
            if os.path.isfile(target_path):
                print(f"delete {target_path}")
                os.remove(target_path)


def reset_migrations():
    for reset_dir in reset_migrations_list:
        reset_migrate(reset_dir)


def setting_directory():
    for reset_target in reset_target_list:
        if not os.path.exists(reset_target):
            os.makedirs(reset_target)


if os.path.isfile("db.sqlite3"):
    os.remove("db.sqlite3")

reset_data()

setting_directory()

# if os.path.exists("static/images/test.png"):
#     os.system("cp static/images/test.png media/user_profile/default_profile.png")

reset_migrations()

os.system("python manage.py makemigrations")

os.system("python manage.py migrate")
