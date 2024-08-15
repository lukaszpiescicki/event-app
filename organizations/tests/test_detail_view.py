from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from core.consts import GROUPS__ORGANIZATION_ADMINS, GROUPS__ORGANIZATION_MEMBERS
from users.factories import UserFactory

from ..factories import OrganizationFactory


class OrganizationDetailViewTestCase(TestCase):
    def setUp(self):
        admins_group = Group.objects.get(name=GROUPS__ORGANIZATION_ADMINS)
        members_group = Group.objects.get(name=GROUPS__ORGANIZATION_MEMBERS)
        self.admin = UserFactory(groups=admins_group)

        self.member = UserFactory(groups=members_group)

        self.organization = OrganizationFactory(owner=self.admin)

    def test_organization_detail_view_when_user_logged_in(self):
        self.client.force_login(self.admin)
        response = self.client.get(
            reverse("organization-detail", kwargs={"pk": self.organization.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["object"], self.organization)
        self.assertTemplateUsed(response, "organizations/organization.html")

    def test_organization_detail_view_when_organization_not_exist(self):
        self.client.force_login(self.admin)
        response = self.client.get(reverse("organization-detail", kwargs={"pk": 999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_organization_detail_view_if_user_is_not_owner(self):
        self.client.force_login(self.member)
        response = self.client.get(
            reverse("organization-detail", kwargs={"pk": self.organization.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.context["object"], self.organization)
        self.assertTemplateUsed(response, "organizations/organization.html")
