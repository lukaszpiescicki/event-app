from blog.factories import ArticleFactory
from blog.models import Article
from django.test import TestCase
from users.models import CustomUser


class TestArticleFactory(TestCase):
    def test_article_factory_creation_single_object(self):
        ArticleFactory.create()
        self.assertEqual(Article.objects.count(), 1)
        self.assertEqual(CustomUser.objects.count(), 1)

    def test_article_factory_creation_bulk_objects(self):
        ArticleFactory.create_batch(5)

        self.assertEqual(Article.objects.count(), 5)
        self.assertEqual(CustomUser.objects.count(), 5)
