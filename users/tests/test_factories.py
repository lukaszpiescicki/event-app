from django.test import TestCase, tag

from users.factories import UserFactory
from users.models import CustomUser


@tag("u")
class TestUsersFactory(TestCase):
    def test_user_factory_creation_single_object(self):
        UserFactory.create()
        self.assertEqual(CustomUser.objects.count(), 1)

    def test_user_factory_creation_bulk_objects(self):
        UserFactory.create_batch(5)

        self.assertEqual(CustomUser.objects.count(), 5)
