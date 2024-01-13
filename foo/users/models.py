from django.db import models
from django.contrib.auth.models import AbstractUser
from music_notes.models import MusicNotes
from organizations.models import Organization
from PIL import Image


class CustomUser(AbstractUser):
    organization = models.ForeignKey(Organization, on_delete=models.DO_NOTHING, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    notes = models.ForeignKey(MusicNotes, on_delete=models.DO_NOTHING, null=True, blank=True),
    instrument = models.CharField(max_length=20, null=True, blank=True)
    voice = models.DecimalField(decimal_places=0, max_digits=1, null=True, blank=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
