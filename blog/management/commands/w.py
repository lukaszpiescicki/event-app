from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def func_add_article_group(self):
        from django.contrib.auth.models import Group, Permission, User
        from django.contrib.contenttypes.models import ContentType

        from organizations.models import Organization

        content_type = ContentType.objects.get_for_model(Organization)
        post_permission = Permission.objects.filter(content_type=content_type)
        print([perm.codename for perm in post_permission])

    def handle(self, *args, **options):
        self.func_add_article_group()
