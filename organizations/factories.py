import factory

from users.factories import UserFactory

from .models import Organization


class OrganizationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Organization

    name = factory.Faker("sentence", nb_words=3)
    city = factory.Faker("city")
    email = factory.Faker("email")
    phone_number = factory.Faker("phone_number")
    owner = factory.SubFactory(UserFactory)

    @factory.post_generation
    def members(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for member in extracted:
                self.members.add(member)
