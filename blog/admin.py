from django.contrib import admin
from .models import Post, Category, Contact, Comment
from django.utils.html import format_html


class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "preview", "image", "created_at", "is_published")
    list_display_links = ("id", "title")

    def preview(self, obj):
        return format_html(f"<img width=50 height=50 src='{obj.image.url}'")


class ContactAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone", "write_message", "created_at", "is_solved")


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'post', 'created_at')


admin.site.register(Post, PostAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Category)
admin.site.register(Comment, CommentAdmin)
