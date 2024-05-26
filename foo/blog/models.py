from django.conf import settings
from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager


class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="blog_articles"
    )
    tags = TaggableManager()

    def total_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse("article-detail", kwargs={"pk": self.pk})

    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100)
    body = models.TextField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["created"]
        indexes = [models.Index(fields=["created"])]

    def __str__(self):
        return f"Comment by {self.author} on {self.article}"
