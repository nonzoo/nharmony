from .models import Post, Comment
from rest_framework import serializers
from account.serializers import UserSerializer

class PostSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Post
        fields = ('id', 'body','likes_count','created_by','comments_count','created_at_formatted')


class CommentSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ('id', 'body','created_by','created_at_formatted','commented_on','created_for')


class PostDetailSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ('id', 'body','likes_count','created_by','comments_count','created_at_formatted','comments')