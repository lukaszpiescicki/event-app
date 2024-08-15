from django.contrib.auth.models import Group
from django.test import TestCase, tag
from django.urls import reverse
from rest_framework import status

from blog.models import Article
from core.consts import GROUPS__AUTHOR
from users.factories import UserFactory

from ..factories import ArticleFactory


class ArticleUpdateViewTestCase(TestCase):
    def setUp(self):
        admin_group = Group.objects.get(name=GROUPS__AUTHOR)
        self.user = UserFactory(groups=admin_group)
        self.user1 = UserFactory(groups=admin_group)

        self.article = ArticleFactory(author=self.user)

    def test_update_article_if_user_logged_in(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("article-update", kwargs={"pk": self.article.pk}),
            {"title": "abcdef", "content": "test content"},
            follow=True,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.article.refresh_from_db()
        article = Article.objects.first()
        self.assertEqual(self.article.title, article.title)

    def test_update_if_one_value_passed(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("article-update", kwargs={"pk": self.article.pk}),
            {"title": "abcdef"},
            follow=True,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.article.refresh_from_db()
        article = Article.objects.first()
        self.assertEqual(self.article.title, article.title)

    def test_update_if_user_not_logged_in(self):
        response = self.client.post(
            reverse("article-update", kwargs={"pk": self.article.pk}),
            {"title": "abcdef", "content": "test content"},
            follow=True,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.article.refresh_from_db()
        article = Article.objects.first()
        self.assertEqual(self.article.title, article.title)

        self.assertRedirects(
            response,
            reverse("login")
            + "?next="
            + reverse("article-update", kwargs={"pk": self.article.pk}),
        )

    @tag("au4")
    def test_update_if_user_is_not_author(self):
        self.client.force_login(self.user1)
        response = self.client.post(
            reverse("article-update", kwargs={"pk": self.article.pk}),
            {"title": "abcdef", "content": "test content"},
            follow=True,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.article.refresh_from_db()
        article = Article.objects.first()
        self.assertEqual(self.article.title, article.title)

    @tag("au5")
    def test_update_if_object_does_not_exist(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("article-update", kwargs={"pk": 100}),
            {"title": "abcdef", "content": "test content"},
            follow=True,
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @tag("au6")
    def test_update_with_incorrect_input_data(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("article-update", kwargs={"pk": self.article.pk}),
            {"title": "", "content": "test content"},
            follow=True,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.article.refresh_from_db()
        article = Article.objects.first()
        self.assertEqual(self.article.title, article.title)
