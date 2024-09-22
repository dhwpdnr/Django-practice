from django.test import TestCase
from soft_delete.models import SoftDelete, Foo, Bar


class SoftDeleteTestCase(TestCase):
    def test_create_and_soft_delete(self):
        """
        1. 객체를 생성하고 soft delete 시킨 이후에 같은 이름으로 생성이 잘 되는지 테스트
        """
        # 객체 생성
        instance = SoftDelete.objects.create(name="test")
        self.assertEqual(instance.name, "test")
        print(f"Created instance: {instance}")

        # Soft delete
        instance.delete()
        self.assertEqual(instance.deleted, True)
        print(f"Soft deleted instance: {instance}")

        # Soft delete 후, 같은 이름으로 새 객체 생성
        new_instance = SoftDelete.objects.create(name="test")
        self.assertEqual(SoftDelete.objects.count(), 1)  # deleted=False인 객체는 1개
        print(f"New instance after soft delete: {new_instance}")

    def test_create_twice_after_soft_delete(self):
        """
        2. 객체를 생성하고 soft delete 시킨 후, 같은 이름으로 두 번 생성 시 unique 제약 조건 확인
        """
        # 객체 생성 및 soft delete
        instance = SoftDelete.objects.create(name="test")
        instance.delete()
        self.assertEqual(instance.deleted, True)

        # 같은 이름으로 객체 첫 번째 생성 (정상)
        new_instance_1 = SoftDelete.objects.create(name="test")
        self.assertEqual(new_instance_1.name, "test")
        print(f"First creation after soft delete: {new_instance_1}")

        # 같은 이름으로 객체 두 번째 생성 (unique 제약 조건으로 인해 실패해야 함)
        with self.assertRaises(Exception):
            SoftDelete.objects.create(name="test")
        print("Second creation with the same name raised an exception as expected.")

    def test_soft_delete_after_creation(self):
        """
        3. 객체를 생성하고 soft delete 시킨 후, 같은 이름으로 다시 생성한 객체를 soft delete 했을 때 unique 제약 조건에 방해받지 않고 삭제되는지 확인
        """
        # 객체 생성 및 soft delete
        instance = SoftDelete.objects.create(name="test")
        instance.delete()
        self.assertEqual(instance.deleted, True)

        # 같은 이름으로 객체 다시 생성
        new_instance = SoftDelete.objects.create(name="test")
        self.assertEqual(new_instance.name, "test")
        print(f"Re-created instance: {new_instance}")

        # 다시 생성한 객체 soft delete
        new_instance.delete()
        self.assertEqual(new_instance.deleted, True)
        print(f"Soft deleted re-created instance: {new_instance}")

        # unique 제약 조건에 방해받지 않고 잘 삭제되는지 확인
        self.assertEqual(SoftDelete.objects.count(), 0)  # deleted=False인 객체는 0개
        print("Soft deleted successfully without unique constraint issues.")

    def test_soft_delete_CASCADE(self):
        """Soft Delete CASCADE 테스트"""
        # 객체 생성
        foo = Foo.objects.create(name="foo")
        bar = Bar.objects.create(name="bar", foo=foo)
        self.assertEqual(Foo.objects.count(), 1)
        self.assertEqual(Bar.objects.count(), 1)

        # foo 객체 soft delete
        foo.delete()
        bar.refresh_from_db()
        self.assertEqual(foo.deleted, True)
        self.assertEqual(bar.deleted, True)
        self.assertEqual(Foo.objects.count(), 0)
        self.assertEqual(Bar.objects.count(), 0)
        print("Soft deleted foo and bar objects successfully with CASCADE.")
