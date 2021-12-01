from django.db.models.fields import SlugField
from rest_framework import serializers
from .models import Post, Comment, Like
from users.serializers import User_Profile, userPSerializer


class PostSerializer(serializers.ModelSerializer):
    #author = serializers.StringRelatedField(source = 'author.username')
    #shared_user = serializers.StringRelatedField(source = 'shared_user.username', many=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'text', 'image', 'pub_date', 'author',
                  'shared_user', 'shared_on', 'privacy', 'contentType')

    def create(self, validated_data):

        return Post.objects.create(**validated_data)

    def update(self, instance, validated_data):

        instance.id = validated_data.get('id', instance.id)
        instance.title = validated_data.get('title', instance.title)
        instance.text = validated_data.get('text', instance.text)
        instance.image = validated_data.get('image', instance.image)
        instance.pub_date = validated_data.get('pub_date', instance.pub_date)
        instance.author = validated_data.get('author', instance.author)
        instance.shared_user = validated_data.get('shared_user',
                                                  instance.shared_user)
        instance.shared_on = validated_data.get('shared_on',
                                                instance.shared_on)
        instance.privacy = validated_data.get('privacy', instance.privacy)
        instance.contentType = validated_data.get('contentType',
                                                  instance.contentType)
        instance.save()
        return instance


class CommentSerializer(serializers.ModelSerializer):

    author = userPSerializer(many=False, read_only=True)

    class Meta:
        model = Comment
        fields = ('type', 'author', 'post', 'comment_body', 'comment_created',
                  'id')


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('user', 'post', 'inbox', 'comment')