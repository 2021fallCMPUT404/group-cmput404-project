from rest_framework import serializers

from .models import User, User_Profile, UserFollows

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
        fields = ['type', 'id', 'url', 'host', 'displayName', 'github', 'bio'] #TODO: ADD URL AND HOST
        read_only_fields = ['type', 'id', 'url', 'host',]
        


class userFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollows
        fields = '__all__'
