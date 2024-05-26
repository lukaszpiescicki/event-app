from core.consts import GROUPS__AUTHOR
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse
from users.factories import UserFactory

from ..factories import ArticleFactory


class ArticleListViewTestCase(TestCase):
    def setUp(self):
        author_group = Group.objects.get(name=GROUPS__AUTHOR)
        self.user = UserFactory(groups=author_group)

        self.article = ArticleFactory(author=self.user)
        self.article1 = ArticleFactory(author=self.user)
        self.article2 = ArticleFactory(author=self.user)

    def test_article_list_view_when_user_logged_in(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("article-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.article, response.context["posts"])
        self.assertIn(self.article1, response.context["posts"])
        self.assertIn(self.article2, response.context["posts"])
        self.assertTemplateUsed(response, "blog/blog.html")
        self.assertEqual(len(response.context["posts"]), 3)
