from datetime import datetime

import factory
from users.factories import UserFactory

from .models import Article


class ArticleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Article

    title = factory.Faker("sentence", nb_words=6)
    content = factory.Faker("paragraph", nb_sentences=5)
    date_posted = factory.LazyFunction(datetime.now)
    author = factory.SubFactory(UserFactory)

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for tag in extracted:
                self.tags.add(tag)

    @factory.post_generation
    def likes(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for like in extracted:
                self.likes.add(like)
