from django.forms.fields import EmailField
from django.test import TestCase
from django.urls import reverse
from django.test.utils import setup_test_environment
from django.contrib.auth import authenticate
from django.test import Client
from .models import Create_user, User, User_Profile, UserFollows, FriendRequest

# Create your tests here.
client = Client()

class FriendRequestModelTests(TestCase):
    user1 = User(username="user1", password="1")
    user1_profile = User_Profile(user=user1)
    user2= User(username="user2", password='2')
    user2_profile = User_Profile(user=user2)


    def test_create_friend_request(self):
        f_req = FriendRequest(actor=self.user1_profile, object=self.user2_profile)
        self.assertIs(f_req.actor == self.user1_profile, True)
        self.assertIs(f_req.object == self.user2_profile, True)


class UserFollowsModelsTests(TestCase):
    user1 = User(username="user1", password="1")
    user1_profile = User_Profile(user=user1)
    user2= User(username="user2", password='2')
    user2_profile = User_Profile(user=user2)

    def test_create_user_follow(self):
        user_follow = UserFollows(actor=self.user1_profile, object=self.user2_profile)
        self.assertIs(user_follow.actor == self.user1_profile, True)
        self.assertIs(user_follow.object == self.user2_profile, True)


class UserViewsTests(TestCase):
    user1 = User(username="user1", password="1", id=1)
    user1_profile = User_Profile(user=user1)
    
    def test_homepage(self):
        response = self.client.get(reverse('users:homepage'))
        self.assertTrue(response.status_code != 404)


    def test_wrong_view_request(self):
        response = self.client.get(reverse('users:view_requests', args=([100])))
        self.assertEqual(response.status_code, 403)