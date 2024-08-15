from django.apps import AppConfig
from django.db.models.signals import post_migrate


def create_default_site_profile(sender, **kwargs) -> None:
    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType

    from .models import Event

    event_participant_group, _ = Group.objects.get_or_create(name="Event Participants")
    event_admin_group, _ = Group.objects.get_or_create(name="Event Admins")

    content_type = ContentType.objects.get_for_model(Event)
    event_permission = Permission.objects.filter(content_type=content_type)

    for perm in event_permission:
        event_admin_group.permissions.add(perm)
        if perm.codename == "view_event":
            event_participant_group.permissions.add(perm)


class EventsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "events"

    def ready(self) -> None:
        post_migrate.connect(create_default_site_profile, sender=self)
