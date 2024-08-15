from django.apps import AppConfig
from django.db.models.signals import post_migrate


def create_default_site_profile(sender, **kwargs) -> None:
    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType

    from organizations.models import Organization

    organization_member_group, _ = Group.objects.get_or_create(
        name="Organization Members"
    )
    organization_admin_group, _ = Group.objects.get_or_create(
        name="Organization Admins"
    )

    content_type = ContentType.objects.get_for_model(Organization)
    music_notes_permission = Permission.objects.filter(content_type=content_type)

    for perm in music_notes_permission:
        organization_admin_group.permissions.add(perm)
        if perm.codename == "view_organization":
            organization_member_group.permissions.add(perm)
            organization_admin_group.permissions.add(perm)


class OrganizationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "organizations"

    def ready(self) -> None:
        post_migrate.connect(create_default_site_profile, sender=self)
