from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions


class UsernamePasswordAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        print(request.META)
        username = request.META.get('username')

        password = request.META.get('password')

        if not username:
            return None
        if not password:
            return None
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        user = User.objects.get(username=username)
        if user.password != password:
            return None

        return (user, None)
