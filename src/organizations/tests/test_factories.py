from django.test import TestCase, tag
from organizations.factories import OrganizationFactory
from organizations.models import Organization


@tag("o")
class TestOrganizationFactory(TestCase):
    def test_organization_factory_creation_single_object(self):
        OrganizationFactory.create()
        self.assertEqual(Organization.objects.count(), 1)

    def test_organization_factory_creation_bulk_objects(self):
        OrganizationFactory.create_batch(5)

        self.assertEqual(Organization.objects.count(), 5)
