from django.test import TestCase
from django.contrib.auth.models import User
from users.models import User_Profile
from django.urls import reverse
from users.views import register
from users.create_user_form import create_new_user, create_new_user_profile
from django.test import Client


class UsersTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create(username='testcase1',
                                    first_name='test1',
                                    last_name='case1',
                                    email='testcase1@ualberta.ca',
                                    password='12345')
        user_profile1 = User_Profile.objects.create(
            displayName='case_1',
            user=user1,
            first_name='test1',
            last_name='case1',
            email='testcase1@ualberta.ca',
            profileImage='test_image.jpg',
            github='JohnChen97',
            bio='test_bio1')

        user2 = User.objects.create(username='testcase2',
                                    first_name='test2',
                                    last_name='case2',
                                    email='testcase2@ualberta.ca',
                                    password='123456')
        user_profile2 = User_Profile.objects.create(
            displayName='case_2',
            user=user2,
            first_name='test2',
            last_name='case2',
            email='testcase2@ualberta.ca',
            profileImage='test_image.jpg',
            github='JohnChen97',
            bio='test_bio2')

    def test_user_profile_model(self):
        """Animals that can speak are correctly identified"""
        test_user_1 = User.objects.get(username="testcase1")
        test_profile_1 = User_Profile.objects.get(user=test_user_1)
        test_user_2 = User.objects.get(username="testcase2")
        test_profile_2 = User_Profile.objects.get(user=test_user_2)
        self.assertEqual(test_profile_1.displayName, 'case_1')
        self.assertEqual(test_profile_2.displayName, 'case_2')

        self.assertEqual(test_profile_1.first_name, 'test1')
        self.assertEqual(test_profile_2.first_name, 'test2')

        self.assertEqual(test_profile_1.last_name, 'case1')
        self.assertEqual(test_profile_2.last_name, 'case2')

        self.assertEqual(test_profile_1.email, 'testcase1@ualberta.ca')
        self.assertEqual(test_profile_2.email, 'testcase2@ualberta.ca')

        self.assertEqual(test_profile_1.bio, 'test_bio1')
        self.assertEqual(test_profile_2.bio, 'test_bio2')

        self.assertEqual(test_profile_1.profileImage.url,
                         '/media/test_image.jpg')
        self.assertEqual(test_profile_2.profileImage.url,
                         '/media/test_image.jpg')

        self.assertEqual(test_profile_1.github,
                         'https://github.com/orgs/2021fallCMPUT404/dashboard')
        self.assertEqual(test_profile_2.github,
                         'https://github.com/JohnChen97/CMPUT404_lab1')

    def test_user_model(self):
        test_user_1 = User.objects.get(username="testcase1")
        test_user_2 = User.objects.get(username="testcase2")

        self.assertEqual(test_user_1.username, 'testcase1')
        self.assertEqual(test_user_2.username, 'testcase2')

        self.assertEqual(test_user_1.first_name, 'test1')
        self.assertEqual(test_user_2.first_name, 'test2')

        self.assertEqual(test_user_1.last_name, 'case1')
        self.assertEqual(test_user_2.last_name, 'case2')

        self.assertEqual(test_user_1.email, 'testcase1@ualberta.ca')
        self.assertEqual(test_user_2.email, 'testcase2@ualberta.ca')

        self.assertEqual(test_user_1.password, '12345')
        self.assertEqual(test_user_2.password, '123456')

    def test_valid_form(self):
        user3 = User.objects.create(username='testcase3',
                                    first_name='test3',
                                    last_name='case3',
                                    email='testcase3@ualberta.ca',
                                    password='12345')
        user_profile3 = User_Profile.objects.create(
            displayName='case_3',
            user=user3,
            first_name='test3',
            last_name='case3',
            email='testcase3@ualberta.ca',
            profileImage='test_image.jpg',
            github='https://github.com/orgs/2021fallCMPUT404/dashboard',
            bio='test_bio3')
        user_data3 = {
            'username': 'testcase5',
            'first_name': user3.first_name,
            'last_name': user3.last_name,
            'email': user3.email,
            'password': '12345',
            'confirm_password': '12345',
        }
        user_profile_data3 = {
            'displayName': user_profile3.displayName,
            'first_name': user_profile3.first_name,
            'last_name': user_profile3.last_name,
            'email': user_profile3.email,
            'profileImage': user_profile3.profileImage,
            'github': user_profile3.github,
            'bio': user_profile3.bio,
        }
        user_form = create_new_user(data=user_data3)
        user_profile_form = create_new_user_profile(data=user_profile_data3)
        print(user_form)
        self.assertTrue(user_form.is_valid())
        self.assertTrue(user_profile_form.is_valid())

    def test_invalid_form(self):
        user4 = User.objects.create(username='testcase4',
                                    first_name='test4',
                                    last_name='case4',
                                    email='testcase4@ualberta.ca',
                                    password='12345')
        user_profile4 = User_Profile.objects.create(
            displayName='case_4',
            user=user4,
            first_name='test4',
            last_name='case4',
            email='testcase4@ualberta.ca',
            profileImage='test_image.jpg',
            github='https://github.com/orgs/2021fallCMPUT404/dashboard',
            bio='test_bio3')
        user_data4 = {
            'username': user4.username,
            'first_name': user4.first_name,
            'last_name': user4.last_name,
            'email': user4.email,
            'password': user4.password,
            'confirm_password': user4.password,
        }
        user_profile_data4 = {
            'displayName': 'false',
            'first_name': 'lol',
            'last_name': 'lol',
            'email': 'lol',
            'profileImage': 'falseImage.png',
            'github': 123,
            'bio': 'fasle_bio',
        }
        user_form = create_new_user(data=user_data4)
        user_profile_form = create_new_user_profile(data=user_profile_data4)

        self.assertFalse(user_form.is_valid())
        self.assertFalse(user_profile_form.is_valid())
