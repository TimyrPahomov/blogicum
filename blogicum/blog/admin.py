from django.contrib import admin

from blog.models import Category, Comment, Location, Post

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Location)
admin.site.register(Comment)
