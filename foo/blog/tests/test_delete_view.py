from blog.models import Article
from core.consts import GROUPS__AUTHOR
from django.contrib.auth.models import Group
from django.test import TestCase, tag
from django.urls import reverse
from rest_framework import status
from users.factories import UserFactory

from ..factories import ArticleFactory


@tag("adel")
class ArticleDeleteViewTestCase(TestCase):
    def setUp(self):
        author_group = Group.objects.get(name=GROUPS__AUTHOR)
        self.user = UserFactory(groups=[author_group])
        self.article = ArticleFactory(author=self.user)

    @tag("adel1")
    def test_delete_article_when_user_is_author(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("article-delete", kwargs={"pk": self.article.pk}), follow=True
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Article.objects.count(), 0)

    @tag("adel2")
    def test_delete_article_which_not_exist(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("article-delete", kwargs={"pk": 999}), follow=True
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @tag("adel3")
    def test_delete_article_when_user_is_not_author(self):
        self.user1 = UserFactory()
        self.client.force_login(self.user1)
        response = self.client.post(
            reverse("article-delete", kwargs={"pk": self.article.pk}), follow=True
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Article.objects.count(), 1)

    @tag("adel4")
    def test_delete_article_when_user_not_logged_in(self):
        response = self.client.post(
            reverse("article-delete", kwargs={"pk": self.article.pk}), follow=True
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertRedirects(
            response,
            reverse("login")
            + "?next="
            + reverse("article-delete", kwargs={"pk": self.article.pk}),
        )
        self.assertEqual(Article.objects.count(), 1)
