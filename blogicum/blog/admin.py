from django.contrib import admin

from blog.models import Category, Comment, Location, Post


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'pub_date',
        'is_published',
        'author',
        'category',
        'location'
    )
    list_editable = (
        'is_published',
        'category',
        'location'
    )
    search_fields = (
        'title', 'author__username'
    )
    list_filter = ('category', 'location')
    empty_value_display = 'Не задано'
    inlines = (CommentInline,)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'description',
        'is_published',
        'slug',
    )
    list_editable = ('is_published',)
    list_filter = ('title', 'slug',)


class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'is_published',
    )
    list_editable = ('is_published',)
    list_filter = ('name',)


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'is_published',
        'author'
    )
    list_editable = ('is_published',)
    search_fields = ('author__username',)


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Comment, CommentAdmin)
