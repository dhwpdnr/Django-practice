from django.test import TestCase
from .models import MyModel


class TestMyModel(TestCase):
    def setUp(self):
        """
        테스트 시작 전에 실행되는 메서드
        """
        self.my_model_instance = MyModel.objects.create(name="test_instance")

    def test_create_instance(self):
        """
        MyModel 객체 생성 테스트
        """
        instance = MyModel.objects.create(name="test")
        self.assertEqual(instance.name, "test")

    def test_model_setup(self):
        """
        MyModel 객체 생성 확인 테스트
        """
        self.assertEqual(self.my_model_instance.name, "test_instance")
