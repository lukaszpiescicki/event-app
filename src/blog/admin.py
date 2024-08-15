from django.contrib import admin

from .models import Article, Comment


class ArticleAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "author")
    search_fields = ("title", "content")


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
