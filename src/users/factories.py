import factory
from django.contrib.auth.models import Group
from factory.fuzzy import FuzzyInteger

from .models import CustomUser


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    username = factory.Faker("user_name")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    phone_number = factory.Faker("phone_number", locale="pl_PL")
    instrument = factory.Faker("sentence", nb_words=1)
    voice = FuzzyInteger(1, 3)

    @factory.post_generation
    def friends(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for friend in extracted:
                self.friends.add(friend)

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            if isinstance(extracted, Group):
                self.groups.add(extracted)
            else:
                for group in extracted:
                    self.groups.add(group)
