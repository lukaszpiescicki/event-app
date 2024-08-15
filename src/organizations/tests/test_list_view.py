from core.consts import GROUPS__ORGANIZATION_ADMINS, GROUPS__ORGANIZATION_MEMBERS
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse
from users.factories import UserFactory

from ..factories import OrganizationFactory


class OrganizationsListViewTestCase(TestCase):
    def setUp(self):
        admins_group = Group.objects.get(name=GROUPS__ORGANIZATION_ADMINS)
        members_group = Group.objects.get(name=GROUPS__ORGANIZATION_MEMBERS)

        self.admin = UserFactory(groups=admins_group)
        self.member = UserFactory(groups=members_group)

        self.organization = OrganizationFactory(owner=self.admin)

        self.organization1 = OrganizationFactory(owner=self.member)

        self.organization2 = OrganizationFactory(owner=self.admin)

    def test_organization_list_view_when_user_logged_in(self):
        self.client.force_login(self.admin)
        response = self.client.get(reverse("organizations-home"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.organization, response.context["organizations"])
        self.assertIn(self.organization1, response.context["organizations"])
        self.assertIn(self.organization2, response.context["organizations"])
        self.assertTemplateUsed(response, "organizations/organizations.html")
        self.assertEqual(len(response.context["organizations"]), 3)
