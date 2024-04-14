from django.contrib import admin
from .models import Post, Tag, Contact, Comment

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Contact)
