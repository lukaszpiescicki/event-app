from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from core.consts import GROUPS__ORGANIZATION_ADMINS, GROUPS__ORGANIZATION_MEMBERS
from organizations.models import Organization
from users.factories import UserFactory

from ..factories import OrganizationFactory


class OrganizationUpdateViewTestCase(TestCase):
    def setUp(self):
        admins_group = Group.objects.get(name=GROUPS__ORGANIZATION_ADMINS)
        members_group = Group.objects.get(name=GROUPS__ORGANIZATION_MEMBERS)
        self.admin = UserFactory(groups=admins_group)
        self.member = UserFactory(groups=members_group)

        self.organization = OrganizationFactory(owner=self.admin)

    def test_update_if_user_logged_in(self):
        self.client.force_login(self.admin)
        response = self.client.post(
            reverse("organization-update", kwargs={"pk": self.organization.pk}),
            {"name": "test"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)

        self.organization.refresh_from_db()

        organization = Organization.objects.get(pk=self.organization.pk)
        self.assertEqual(self.organization.name, organization.name)

    def test_update_if_one_value_passed(self):
        self.client.force_login(self.admin)
        response = self.client.post(
            reverse("organization-update", kwargs={"pk": self.organization.pk}),
            {"name": "test"},
            follow=True,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.organization.refresh_from_db()
        organization = Organization.objects.get(pk=self.organization.pk)
        self.assertEqual(self.organization.name, organization.name)

    def test_update_if_user_is_not_author(self):
        self.client.force_login(self.member)
        response = self.client.post(
            reverse("organization-update", kwargs={"pk": self.organization.pk}),
            {"name": "name"},
            follow=True,
        )
        self.assertEqual(response.status_code, 403)
        self.organization.refresh_from_db()
        organization = Organization.objects.get(pk=self.organization.pk)
        self.assertEqual(self.organization.name, organization.name)

    def test_update_if_object_does_not_exist(self):
        self.client.force_login(self.admin)
        response = self.client.post(
            reverse("organization-update", kwargs={"pk": 100}),
            {"name": "name"},
            follow=True,
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_if_user_not_logged_in(self):
        response = self.client.post(
            reverse("organization-update", kwargs={"pk": self.organization.pk}),
            {"name": "test"},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)

        self.organization.refresh_from_db()
        organization = Organization.objects.get(pk=self.organization.pk)
        self.assertEqual(self.organization.name, organization.name)
        self.assertRedirects(
            response,
            reverse("login")
            + "?next="
            + reverse("organization-update", kwargs={"pk": self.organization.pk}),
        )

    def test_update_with_incorrect_input_data(self):
        self.client.force_login(self.admin)
        response = self.client.post(
            reverse("organization-update", kwargs={"pk": self.organization.pk}),
            {"name": ""},
            follow=True,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        organization = Organization.objects.get(pk=self.organization.pk)
        self.assertEqual(self.organization.name, organization.name)
