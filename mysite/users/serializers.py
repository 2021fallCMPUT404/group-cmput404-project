from rest_framework import serializers

from .models import User, User_Profile, UserFollows

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class userPSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Profile
        fields = '__all__'


class userFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollows
        fields = '__all__'