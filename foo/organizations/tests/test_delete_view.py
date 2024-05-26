from core.consts import GROUPS__ORGANIZATION_ADMINS, GROUPS__ORGANIZATION_MEMBERS
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse
from organizations.models import Organization
from rest_framework import status
from users.factories import UserFactory

from ..factories import OrganizationFactory


class OrganizationDeleteViewTestCase(TestCase):
    def setUp(self) -> None:
        admins_group = Group.objects.get(name=GROUPS__ORGANIZATION_ADMINS)
        members_group = Group.objects.get(name=GROUPS__ORGANIZATION_MEMBERS)
        self.admin = UserFactory.create(groups=admins_group)
        self.member = UserFactory.create(groups=members_group)

        self.organization = OrganizationFactory(owner=self.admin)

    def test_delete_event_when_user_is_admin(self):
        self.client.force_login(self.admin)
        response = self.client.post(
            reverse("organization-delete", kwargs={"pk": self.organization.pk}),
            follow=True,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Organization.objects.count(), 0)

    def test_delete_organization_which_not_exist(self):
        self.client.force_login(self.admin)
        response = self.client.post(
            reverse("organization-delete", kwargs={"pk": 999}), follow=True
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_organization_when_user_is_not_owner(self):
        self.client.force_login(self.member)
        response = self.client.post(
            reverse("organization-delete", kwargs={"pk": self.organization.pk}),
            follow=True,
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Organization.objects.count(), 1)

    def test_delete_organization_when_user_not_logged_in(self):
        response = self.client.post(
            reverse("organization-delete", kwargs={"pk": self.organization.pk}),
            follow=True,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertRedirects(
            response,
            reverse("login")
            + "?next="
            + reverse("organization-delete", kwargs={"pk": self.organization.pk}),
        )
        self.assertEqual(Organization.objects.count(), 1)
