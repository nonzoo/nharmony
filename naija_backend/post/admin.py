from django.contrib import admin

from .models import Post, PostAttachment, Like, Comment





admin.site.register(PostAttachment)

@admin.register(Post)
class Post(admin.ModelAdmin):
    list_display = ('body', 'likes_count','comments_count')

@admin.register(Comment)
class Comment(admin.ModelAdmin):
    search_fields = ['commented_on']

@admin.register(Like)
class Like(admin.ModelAdmin):
    list_display = ('created_by', 'created_for', 'created_at')
    list_per_page = 50


