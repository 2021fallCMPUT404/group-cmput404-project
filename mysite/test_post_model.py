from django.test import TestCase
from requests.sessions import TooManyRedirects
from test_users_model_form import *
from posts.models import Post, Comment
from users.serializers import UserSerializer
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
            first_name='test',
            last_name='case',
            email='testcase@ualberta.ca',
            profileImage='test_image.jpg',
            github='JohnChen97',
            bio='test_bio1')

        test_user_1 = User.objects.get(username="testcase")
        test_profile_1 = User_Profile.objects.get(user=test_user_1)

        Post.objects.create(
            #type = 'post',
            text = 'trial',
            image='test_image.jpg',
            author=test_user_1,
            shared_user = None,
            shared_on = None)
        test_post_1 = Post.objects.get(author = test_user_1)
        user_serializer = UserSerializer(user1)
        user_data = user_serializer.data
        Comment.objects.create(post = test_post_1, author = user_data, comment_body = 'test_comment_body')
            

    def test_post_cases(self):
        test_user_1 = User.objects.get(username = "testcase")
        test_profile_1 = User_Profile.objects.get(user = test_user_1)
        test_ps = Post.objects.get(author=test_user_1)
        self.assertEqual(test_ps.text, 'trial')
        self.assertEqual(test_ps.image, 'test_image.jpg')
    
    def test_comment(self):
        test_user_1 = User.objects.get(username = "testcase")
        test_profile_1 = User_Profile.objects.get(user = test_user_1)
        test_ps = Post.objects.get(author=test_user_1)
        test_comment = Comment.objects.get(post = test_ps)
        self.assertEqual(test_comment.comment_body, 'test_comment_body')
    