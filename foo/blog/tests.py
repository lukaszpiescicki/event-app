from django.test import TestCase
from django.urls import reverse, reverse_lazy
from rest_framework import status
from blog.models import Article
from users.models import CustomUser


class ArticleCreateViewTestCase(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(username='tomaszbak', first_name='Tomasz', last_name='Bak',
                                              password='123456')
        self.client.force_login(self.user)

        self.user1 = CustomUser(username='filipraczek', first_name='Filip', last_name='Raczek', password='qwerty')
        self.client.force_login(self.user1)

    #
    #     article = Article.objects.create(
    #         title='article-title',
    #         content='content testowy',
    #         date_posted='2020-05-04',
    #         author=author
    #     )
    #     article1 = Article.objects.create(
    #         title='tytul-artykulu',
    #         content='testtesttest',
    #         date_posted='2137-05-04',
    #         author=author1
    #     )

    def test_get_all_articles_when_db_is_empty(self):
        response = self.client.get(
            reverse(
                'article-list'
            )
        )
        context = response.context
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(context['posts']), 0
        )
        self.assertTemplateUsed(response, 'blog/article_list.html')

    def test_post_article_redirect_if_user_not_logged_in(self):
        self.client.logout()
        response = self.client.get(
            reverse(
                'article-create'
            )
        )
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(
            response, '/login/?next=%2Farticle%2Fnew%2F'
        )

    def test_post_article_correct_render_page_and_returns_200_when_user_logged_in(self):
        response = self.client.get(
            reverse(
                'article-create'
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'blog/article_form.html')

    def test_post_article_correct_object_created(self):
        response = self.client.post(
            reverse(
                'article-create'
            ), {'title': 'test title', 'content': 'test content'}
        )
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        self.assertEqual(Article.objects.count(), 1)
        article = Article.objects.first()
        self.assertEqual(article.title, 'test title')
        self.assertEqual(article.content, 'test content')
        self.assertEqual(article.author, self.user)

    def test_post_article_with_incorrect_input_data(self):
        response = self.client.post(
            reverse(
                'article-create'
            ), {'title': '', 'content': 'test content'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Article.objects.count(), 0)


class ArticleUpdateViewTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username='tomaszbak', first_name='Tomasz', last_name='Bak',
                                              password='123456')
        self.client.force_login(self.user)

        self.user1 = CustomUser(username='filipraczek', first_name='Filip', last_name='Raczek', password='qwerty')
        self.client.force_login(self.user1)

        self.article = Article.objects.create(
            title='article-title',
            content='content testowy'
        )

    def test_update_article_if_user_logged_in(self):
        response = self.client.post(
            reverse(
                'article-update', kwargs={'pk': self.article.pk}
            ), {"title": "abcdef"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.article.title, 'abcdef')
