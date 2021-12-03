from rest_framework import *
from rest_framework import serializers

from .models import FriendRequest, User, User_Profile, UserFollows, Inbox


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        #fields = '__all__'
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        user_profile = User_Profile.objects.get(user=instance)
        user_profile = userPSerializer(user_profile)
        print(user_profile.data)
        ret.update(user_profile.data)
        #ret['profileImage'] = user_profile.data
        
        ret['url'] = "https://cmput404-socialdist-project.herokuapp.com/author/{}".format(str(instance.id))
        ret['host'] = 'https://cmput404-socialdist-project.herokuapp.com/'
        return ret
    '''
    def validate(self, data):
        if not User.objects.get(data['author']).exists:
            raise serializers.ValidationError("The author is None")
        return data
    '''

#User profile serializer
#TODO: Maybe add a full user profile serialzier that includes all fields
class userPSerializer(serializers.ModelSerializer):
    #This puts in the type attribute since __all__ is not grabbing User_Profile.type attribute for some reason
    #Reference: https://stackoverflow.com/a/60891077
    

    class Meta:
        model = User_Profile
        fields = [
            'type', 'id', 'url', 'host', 'displayName', 'github', 'bio',
            'profileImage', 'user'
        ]  #TODO: ADD URL AND HOST
        read_only_fields = ['type', 'id', 'url', 'host', 'user']

class userFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollows
        fields = '__all__'


class friend_request_serializer(serializers.ModelSerializer):
    type = 'Follow'
    actor = userPSerializer(many=False, read_only=True)
    object = userPSerializer(many=False, read_only=True)
    summary = "{} wants to follow {}".format(actor.data['displayName'],
                                             object.data['displayName'])

    class Meta:
        model = FriendRequest
        fields = [
            'type',
            'summary',
            'actor',
            'object',
        ]

class InboxSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Inbox()
        fields = ['type', 'author']
        