from rest_framework import serializers
from django.contrib.auth.models import User
from .models import User_Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email')

    def create(self, validated_data):

        return Post.objects.create(**validated_data)

    def update(self, instance, validated_data):
        #'first_name', 'last_name', 'username', 'email', 'password'
        instance.id = validated_data.get('id', instance.id)
        instance.first_name = validated_data.get('first_name',
                                                 instance.first_name)
        instance.last_name = validated_data.get('last_name',
                                                instance.last_name)
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        #instance.password = validated_data.get('password', instance.password)

        instance.save()
        return instance


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Profile
        fields = ('id', 'displayName', 'github', 'profileImage', 'bio')

    def create(self, validated_data):

        return Post.objects.create(**validated_data)

    def update(self, instance, validated_data):
        #'displayName', 'github', 'profileImage', 'bio'
        instance.id = validated_data.get('id', instance.id)
        instance.displayName = validated_data.get('displayName',
                                                  instance.displayName)
        instance.github = validated_data.get('github', instance.github)
        instance.profileImage = validated_data.get('profileImage',
                                                   instance.profileImage)
        instance.bio = validated_data.get('bio', instance.bio)

        instance.save()
        return instance


class InboxProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inbox
        field = author

class 