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

    
    class Meta:
        model = User_Profile
        fields = ['type', 'id', 'url', 'host', 'displayName', 'github', 'bio', 'profileImage', 'user'] #TODO: ADD URL AND HOST
        read_only_fields = ['type', 'id', 'url', 'host','user']
        


class userFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollows
        fields = '__all__'


class friend_request_serializer(serializers.ModelSerializer):

    actor = userPSerializer(many=False, read_only=True)
    object = userPSerializer(many=False, read_only=True)


    class Meta:
        model = FriendRequest
        fields = '__all__'
