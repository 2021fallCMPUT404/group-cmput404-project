from typing import Text
from django.test import TestCase
from posts.models import Post


class AnimalTestCase(TestCase):
    def setUp(self):
        post = Post.objects.create(title='testcase',
                                   text='test',
                                   image='case',
                                   )
        Post.objects.create(
            displayName='case_1',
            profileImage='test_image.jpg',
            github='https://github.com/orgs/2021fallCMPUT404/dashboard',
            bio='test_bio')

    def test_users_model_displayName(self):
        """Animals that can speak are correctly identified"""
        test_user_1 = Post.objects.get(name="testcase")
        test_profile_1 = Post.objects.get(user=test_user_1)
        self.assertEqual(test_profile_1.__str__(), 'case_1')
