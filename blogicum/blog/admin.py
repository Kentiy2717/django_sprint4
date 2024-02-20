from django.contrib import admin

from .models import Category, Location, Post, Comment


class CategoryInline(admin.TabularInline):
    model = Post
    extra = 0


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'is_published',
        'created_at',
    )
    list_editable = (
        'is_published',
    )
    search_fields = ('name',)
    list_filter = ('is_published',)
    list_display_links = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = (
        CategoryInline,
    )
    list_display = (
        'title',
        'is_published',
        'description',
        'slug',
        'created_at',
    )
    list_editable = (
        'is_published',
        'description',
        'slug',
    )
    search_fields = ('title',)
    list_filter = ('is_published', 'title',)
    list_display_links = ('title',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'is_published',
        'text',
        'pub_date',
        'author',
        'location',
        'category',
        'created_at',
        'image',
    )
    list_editable = (
        'is_published',
        'text',
        'pub_date',
        'location',
        'category',
    )
    search_fields = ('title',)
    list_filter = ('is_published', 'pub_date',)
    list_display_links = ('title',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'post',
        'text',
        'author',
        'created_at',
    )
    list_editable = (
        'text',
    )
    search_fields = ('post',)
    list_filter = ('created_at',)
    list_display_links = ('post',)
