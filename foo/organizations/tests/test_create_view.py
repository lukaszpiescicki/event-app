from core.consts import GROUPS__ORGANIZATION_ADMINS, GROUPS__ORGANIZATION_MEMBERS
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse
from organizations.models import Organization
from rest_framework import status
from users.factories import UserFactory


class OrganizationCreateViewTestCase(TestCase):
    def setUp(self):
        admin_group = Group.objects.get(name=GROUPS__ORGANIZATION_ADMINS)
        members_group = Group.objects.get(name=GROUPS__ORGANIZATION_MEMBERS)
        self.admin = UserFactory(groups=admin_group)
        self.member = UserFactory(groups=members_group)

    def test_get_all_organization_when_db_is_empty(self):
        self.client.force_login(user=self.admin)
        response = self.client.get(reverse("organizations-home"))
        context = response.context
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(context["organizations"]), 0)
        self.assertTemplateUsed(response, "organizations/organizations.html")

    def test_create_organization_if_user_not_logged_in(self):
        response = self.client.get(reverse("organization-create"))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(response, "/login/?next=/organization/new/")

    def test_create_organization_render_page_and_return_200_when_user_logged_in(self):
        self.client.force_login(user=self.admin)
        response = self.client.get(reverse("organization-create"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "organizations/organization_form.html")

    def test_create_organization_correct_object_created(self):
        self.client.force_login(user=self.admin)
        response = self.client.post(
            reverse("organization-create"),
            {
                "name": "<NAME>",
                "city": "City",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Organization.objects.count(), 1)
        organization = Organization.objects.first()
        self.assertEqual(organization.name, "<NAME>")
        self.assertEqual(organization.city, "City")
        # self.assertEqual(organization.owner, self.admin)

    def test_create_organization_with_incorrect_input_data(self):
        self.client.force_login(user=self.admin)
        self.assertEqual(Organization.objects.count(), 0)
        response = self.client.post(
            reverse("organization-create"), {"name": "", "city": ""}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Organization.objects.count(), 0)
