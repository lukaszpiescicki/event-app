from django.apps import AppConfig
from django.db.models.signals import post_migrate


def create_default_site_profile(sender, **kwargs) -> None:
    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType
    from music_notes.models import MusicNotes

    music_notes_user_group, _ = Group.objects.get_or_create(name="Music-Notes Users")
    music_notes_admin_group, _ = Group.objects.get_or_create(name="Music-Notes Admins")

    content_type = ContentType.objects.get_for_model(MusicNotes)
    music_notes_permission = Permission.objects.filter(content_type=content_type)

    for perm in music_notes_permission:
        music_notes_admin_group.permissions.add(perm)
        if perm.codename == "view_music_notes":
            music_notes_user_group.permissions.add(perm)
            music_notes_admin_group.permissions.add(perm)


class MusicNotesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "music_notes"

    def ready(self) -> None:
        post_migrate.connect(create_default_site_profile, sender=self)
