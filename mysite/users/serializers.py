from rest_framework import serializers

from .models import User, User_Profile, UserFollows

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

#User profile serializer
class userPSerializer(serializers.ModelSerializer):
    #This puts in the type attribute since __all__ is not grabbing User_Profile.type attribute for some reason
    #Reference: https://stackoverflow.com/a/60891077
    type = serializers.SerializerMethodField('new_field_method')
    def new_field_method(self, modelPointer_):
        return "author"
    class Meta:
        model = User_Profile
        fields = '__all__'
        


class userFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollows
        fields = '__all__'