from django.forms.fields import EmailField
from django.test import TestCase
<<<<<<< HEAD
from django.contrib.auth.models import User
from .models import User_Profile


class UsersTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create(username='testcase',
                                    first_name='test',
                                    last_name='case',
                                    email='testcase@ualberta.ca',
                                    password='12345')
        User_Profile.objects.create(
            displayName='case_1',
            user=user1,
            profileImage='test_image.jpg',
            github='https://github.com/orgs/2021fallCMPUT404/dashboard',
            bio='test_bio1')

        user2 = User.objects.create(username='testcase2',
                                    first_name='test2',
                                    last_name='case2',
                                    email='testcase2@ualberta.ca',
                                    password='123456')
        User_Profile.objects.create(
            displayName='case_2',
            user=user2,
            profileImage='test_image.jpg',
            github='https://github.com/orgs/2021fallCMPUT404/dashboard',
            bio='test_bio2')

    def test_user_model(self):
        """Animals that can speak are correctly identified"""
        test_user_1 = User.objects.get(username="testcase")
        test_profile_1 = User_Profile.objects.get(user=test_user_1)
        test_user_2 = User.objects.get(username="testcase2")
        test_profile_2 = User_Profile.objects.get(user=test_user_2)
        self.assertEqual(test_profile_1.displayName, 'case_1')
        self.assertEqual(test_profile_2.displayName, 'case_2')

        self.assertEqual(test_profile_1.bio, 'test_bio1')
        self.assertEqual(test_profile_2.bio, 'test_bio2')

        self.assertEqual(test_profile_1.profileImage, 'test_image.jpg')
        self.assertEqual(test_profile_2.profileImage, 'test_image.jpg')

        self.assertEqual(test_profile_1.github,
                         'https://github.com/orgs/2021fallCMPUT404/dashboard')
        self.assertEqual(test_profile_2.github,
                         'https://github.com/orgs/2021fallCMPUT404/dashboard')
        '''
        self.assertEqual(test_profile_1.displayName, 'case_1')
        self.assertEqual(test_profile_2.displayName, 'case_2')
        '''
=======
from django.urls import reverse
from django.test.utils import setup_test_environment
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
    
    def test_homepage(self):
        response = self.client.get(reverse('users:homepage'))
        self.assertTrue(response.status_code != 404)

>>>>>>> f03a138ddd73cc0a366506103e575fb55a2e23a5
