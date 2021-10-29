from django.test import TestCase
from .test_users_models import *
from posts.models import Post, Comment

class test_post(TestCase):
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

        test_user_1 = User.objects.get(username="testcase")
        test_profile_1 = User_Profile.objects.get(user=test_user_1)

        Post.objects.create{
            #type = 'post',
            text = 'trial',
            image='test_image.jpg',
            pub_date = models.DateTimeField(auto_now_add=True),
            author = test_profile_1.displayName,
            shared_user = None,
            shared_on = None,
            privacy=models.IntegerField(choices=Privacy,default=PUBLIC),
            visible=None)

            

    def test_post_cases(self):
        test_ps = Post.objects.get(author='case_1')
        self.assertEqual(test_ps.text, 'trial')
        self.assertEqual(test_ps.image, 'test_image.jpg')

    def test_comment(self):
        pass
