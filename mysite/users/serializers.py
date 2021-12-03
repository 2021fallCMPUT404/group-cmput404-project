from rest_framework import *
from rest_framework import serializers

from .models import FriendRequest, User, User_Profile, UserFollows

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

#User profile serializer
#TODO: Maybe add a full user profile serialzier that includes all fields
class userPSerializer(serializers.ModelSerializer):
    #This puts in the type attribute since __all__ is not grabbing User_Profile.type attribute for some reason
    #Reference: https://stackoverflow.com/a/60891077

    url = serializers.SerializerMethodField('get_url')

    
    class Meta:
        model = User_Profile
        fields = ['type', 'id', 'url', 'host', 'displayName', 'email', 'first_name', 
        'last_name', 'github', 'bio', 'profileImage', 'user'] #TODO: ADD URL AND HOST
        read_only_fields = ['type', 'id', 'url', 'host','user', 'profileImage']
        

    def get_url(self, obj):
        return obj.get_absolute_url()

class userFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollows
        fields = '__all__'


class friend_request_serializer(serializers.ModelSerializer):
    type = 'Follow'
    actor = userPSerializer(many=False, read_only=True)
    object = userPSerializer(many=False, read_only=True)
    summary = "{} wants to follow {}".format(actor.data['displayName'], object.data['displayName'])

    class Meta:
        model = FriendRequest
        fields = ['type', 'summary', 'actor', 'object', ]
