from blog.models import Article
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from users.models import CustomUser


class ArticleCreateViewTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            username="tomaszbak",
            first_name="Tomasz",
            last_name="Bak",
            password="123456",
        )
        self.client.force_login(self.user)

        self.user1 = CustomUser.objects.create(
            username="filipraczek",
            first_name="Filip",
            last_name="Raczek",
            password="qwerty",
        )

    def test_get_all_articles_when_db_is_empty(self):
        response = self.client.get(reverse("article-list"))
        context = response.context
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(context["posts"]), 0)
        self.assertTemplateUsed(response, "blog/blog.html")

    def test_post_article_redirect_if_user_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("article-create"))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(response, "/login/?next=%2Farticle%2Fnew%2F")

    def test_post_article_correct_render_page_and_returns_200_when_user_logged_in(self):
        response = self.client.get(reverse("article-create"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "blog/article_form.html")

    def test_post_article_correct_object_created(self):
        response = self.client.post(
            reverse("article-create"),
            {"title": "test title", "content": "test content"},
        )
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        self.assertEqual(Article.objects.count(), 1)
        article = Article.objects.first()
        self.assertEqual(article.title, "test title")
        self.assertEqual(article.content, "test content")
        self.assertEqual(article.author, self.user)

    def test_post_article_with_incorrect_input_data(self):
        response = self.client.post(
            reverse("article-create"), {"title": "", "content": "test content"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Article.objects.count(), 0)


class ArticleUpdateViewTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            username="tomaszbak",
            first_name="Tomasz",
            last_name="Bak",
            password="123456",
        )

        self.user1 = CustomUser.objects.create(
            username="filipraczek",
            first_name="Filip",
            last_name="Raczek",
            password="qwerty",
        )

        self.article = Article.objects.create(
            title="article-title", content="content testowy", author=self.user
        )

    def test_update_article_if_user_logged_in(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("article-update", kwargs={"pk": self.article.pk}),
            {"title": "abcdef", "content": "test content"},
            follow=True,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.article.refresh_from_db()

        self.assertEqual(self.article.title, "abcdef")

    def test_update_if_one_value_passed(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("article-update", kwargs={"pk": self.article.pk}),
            {"title": "abcdef"},
            follow=True,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.article.refresh_from_db()

        self.assertEqual(self.article.title, "article-title")

    def test_update_if_user_not_logged_in(self):
        response = self.client.post(
            reverse("article-update", kwargs={"pk": self.article.pk}),
            {"title": "abcdef", "content": "test content"},
            follow=True,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.article.refresh_from_db()

        self.assertEqual(self.article.title, "article-title")

        self.assertRedirects(
            response,
            reverse("login")
            + "?next="
            + reverse("article-update", kwargs={"pk": self.article.pk}),
        )

    def test_update_if_user_is_not_author(self):
        self.client.force_login(self.user1)
        response = self.client.post(
            reverse("article-update", kwargs={"pk": self.article.pk}),
            {"title": "abcdef", "content": "test content"},
            follow=True,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.article.refresh_from_db()

        self.assertEqual(self.article.title, "article-title")

    def test_update_if_object_does_not_exist(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("article-update", kwargs={"pk": 100}),
            {"title": "abcdef", "content": "test content"},
            follow=True,
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_with_incorrect_input_data(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("article-update", kwargs={"pk": self.article.pk}),
            {"title": "", "content": "test content"},
            follow=True,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.article.refresh_from_db()

        self.assertEqual(self.article.title, "article-title")


class ArticleDeleteViewTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            username="tomaszbak",
            first_name="Tomasz",
            last_name="Bak",
            password="123456",
        )

        self.user1 = CustomUser.objects.create(
            username="filipraczek",
            first_name="Filip",
            last_name="Raczek",
            password="qwerty",
        )

        self.article = Article.objects.create(
            title="article-title", content="content testowy", author=self.user
        )

    def test_delete_article_when_user_is_author(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("article-delete", kwargs={"pk": self.article.pk}), follow=True
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Article.objects.count(), 0)

    def test_delete_article_which_not_exist(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("article-delete", kwargs={"pk": 999}), follow=True
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_article_when_user_is_not_author(self):
        self.client.force_login(self.user1)
        response = self.client.post(
            reverse("article-delete", kwargs={"pk": self.article.pk}), follow=True
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Article.objects.count(), 1)

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


class ArticleListViewTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            username="tomaszbak",
            first_name="Tomasz",
            last_name="Bak",
            password="123456",
        )

        self.user1 = CustomUser.objects.create(
            username="filipraczek",
            first_name="Filip",
            last_name="Raczek",
            password="qwerty",
        )

        self.article = Article.objects.create(
            title="article-title", content="content testowy", author=self.user
        )

        self.article1 = Article.objects.create(
            title="article-1", content="content 1", author=self.user1
        )

        self.article2 = Article.objects.create(
            title="article-2", content="content 2", author=self.user
        )

    def test_article_list_view_when_user_logged_in(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("article-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.article1, response.context["posts"])
        self.assertIn(self.article2, response.context["posts"])
        self.assertIn(self.article, response.context["posts"])
        self.assertTemplateUsed(response, "blog/blog.html")
        self.assertEqual(len(response.context["posts"]), 3)


class ArticleDetailViewTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            username="tomaszbak",
            first_name="Tomasz",
            last_name="Bak",
            password="123456",
        )

        self.user1 = CustomUser.objects.create(
            username="filipraczek",
            first_name="Filip",
            last_name="Raczek",
            password="qwerty",
        )

        self.article = Article.objects.create(
            title="article-title", content="content testowy", author=self.user
        )

    def test_article_detail_view_when_user_logged_in(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse("article-detail", kwargs={"pk": self.article.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["object"], self.article)
        self.assertTemplateUsed(response, "blog/article.html")

    def test_article_detail_view_when_article_not_exist(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("article-detail", kwargs={"pk": 999}))
        self.assertEqual(response.status_code, 404)

    def test_article_detail_view_if_user_is_not_author(self):
        self.client.force_login(self.user1)
        response = self.client.get(
            reverse("article-detail", kwargs={"pk": self.article.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["object"], self.article)
        self.assertTemplateUsed(response, "blog/article.html")
