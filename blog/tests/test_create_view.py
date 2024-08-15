from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from blog.models import Article
from core.consts import GROUPS__AUTHOR
from users.factories import UserFactory


class ArticleCreateViewTestCase(TestCase):
    def setUp(self):
        author_group = Group.objects.get(name=GROUPS__AUTHOR)
        self.user = UserFactory(groups=author_group)

    def test_get_all_articles_when_db_is_empty(self):
        response = self.client.get(reverse("article-list"))
        context = response.context
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(context["posts"]), 0)
        self.assertTemplateUsed(response, "blog/blog.html")

    def test_post_article_redirect_if_user_not_logged_in(self):
        response = self.client.get(reverse("article-create"))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(response, "/login/?next=/articles/new/")

    def test_post_article_correct_render_page_and_returns_200_when_user_logged_in(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("article-create"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "blog/article_form.html")

    def test_post_article_correct_object_created(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("article-create"),
            {"title": "test title", "content": "test content"},
        )
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        self.assertEqual(Article.objects.count(), 1)
        first_article = Article.objects.first()
        self.assertEqual(first_article.title, "test title")
        self.assertEqual(first_article.content, "test content")
        self.assertEqual(first_article.author, self.user)

    def test_post_article_with_incorrect_input_data(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("article-create"), {"title": "", "content": "test content"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Article.objects.count(), 0)
