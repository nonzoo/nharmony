from .models import Post, Comment, Trend, PostAttachment
from rest_framework import serializers
from account.serializers import UserSerializer


class PostAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostAttachment
        fields = ('id','get_image',)

class PostSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    attachments = PostAttachmentSerializer(read_only=True, many=True)
    class Meta:
        model = Post
        fields = ('id', 'body','likes_count','created_by','comments_count','created_at_formatted','attachments',)


class CommentSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ('id', 'body','created_by','created_at_formatted','commented_on','created_for')


class PostDetailSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    attachments = PostAttachmentSerializer(read_only=True, many=True)
    class Meta:
        model = Post
        fields = ('id', 'body','likes_count','created_by','comments_count','created_at_formatted','comments','attachments')



class TrendSerializer(serializers.ModelSerializer):
    class Meta:
        model= Trend
        fields = ('id','hashtag','occurences')