from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from core.consts import GROUPS__AUTHOR
from users.factories import UserFactory

from ..factories import ArticleFactory


class ArticleDetailViewTestCase(TestCase):
    def setUp(self):
        author_group = Group.objects.get(name=GROUPS__AUTHOR)
        self.user = UserFactory(groups=[author_group])
        self.user1 = UserFactory(groups=[author_group])
        self.article = ArticleFactory(author=self.user)

    def test_article_detail_view_when_user_logged_in(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("article-detail", kwargs={"pk": self.article.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.context["object"], self.article)
        self.assertTemplateUsed(response, "blog/article.html")

    def test_article_detail_view_when_article_not_exist(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("article-detail", kwargs={"pk": 999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_article_detail_view_if_user_is_not_author(self):
        self.client.force_login(self.user1)
        response = self.client.get(
            reverse("article-detail", kwargs={"pk": self.article.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.context["object"], self.article)
        self.assertTemplateUsed(response, "blog/article.html")
