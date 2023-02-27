from django.contrib import admin

from .models import Author, Comment, Post, Tags


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ("title", "author", "date")
    list_display = ("title", "author", "date")


class CommentAdmin(admin.ModelAdmin):
    list_display = ("user_name", "post")


admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Tags)
admin.site.register(Comment, CommentAdmin)
