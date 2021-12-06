from django.db.models.fields import SlugField
from rest_framework import serializers
from .models import Post, Comment, Like, Node
from users.serializers import User_Profile, userPSerializer


class PostSerializer(serializers.ModelSerializer):
    #author = serializers.StringRelatedField(source = 'author.username')
    #shared_user = serializers.StringRelatedField(source = 'shared_user.username', many=True)

    class Meta:
        model = Post
        fields = ('title', 'content', 'image', 'published', 'author',
                  'shared_user', 'visibility', 'contentType', 'unlisted','description', )

    def create(self, validated_data):

        return Post.objects.create(**validated_data)

    def update(self, instance, validated_data):

        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.image = validated_data.get('image', instance.image)
        instance.published = validated_data.get('published', instance.published)
        instance.author = validated_data.get('author', instance.author)
        instance.shared_user = validated_data.get('shared_user',
                                                  instance.shared_user)
        instance.shared_on = validated_data.get('shared_on',
                                                instance.shared_on)
        instance.visibility = validated_data.get('visibility', instance.visibility)
        instance.contentType = validated_data.get('contentType',
                                                  instance.contentType)
        instance.save()
        return instance


class CommentSerializer(serializers.ModelSerializer):

    author = userPSerializer(many=False, read_only=True)
    class Meta:
        model = Comment
        fields = ('type', 'author', 'post', 'comment_body', 'comment_created', 'id')


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('user', 'post')


class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ['team_id','users','posts', 'username','password']