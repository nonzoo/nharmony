from .models import User,FriendRequest,Categories
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email','age','friends_count','posts_count','get_avatar','gender','locations','bio')

class FriendRequestSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only = True)

    class Meta:
        model = FriendRequest
        fields = ('id','created_by',)

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'

