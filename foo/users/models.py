from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    instrument = models.CharField(max_length=20, null=True, blank=True)
    voice = models.DecimalField(decimal_places=0, max_digits=1, null=True, blank=True)
    image = models.ImageField(
        default="default.jpg", upload_to="profile_pics", null=True, blank=True
    )
    friends = models.ManyToManyField("CustomUser", blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class FriendRequest(models.Model):
    from_user = models.ForeignKey(
        CustomUser, related_name="from_user", on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        CustomUser, related_name="to_user", on_delete=models.CASCADE
    )
