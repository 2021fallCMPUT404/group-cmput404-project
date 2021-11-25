from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Post, Comment, Like
from .serializers import PostSerializer

client = Client()

class PostTest(TestCase):
    def setUp(self):
        Post.objects.create(title="Post 1", text="This is post 1", image=None, privacy=1, contentType=1)
        Post.objects.create(title="Post 2", text="This is post 2", image=None, privacy=1, contentType=0)
    
    def test_add_post(self):
        self.assertEqual(len(Post.objects.all()),2)
        Post.objects.create(title="Post 3", text="*This is post 3*", image=None, privacy=1, contentType=1)
        self.assertEqual(len(Post.objects.all()),3)

    def test_edit_post(self):
        p1 = Post.objects.get(title="Post 1")
        p1.text = "Post 1 is here"
        p1.save()
        self.assertEqual(Post.objects.get(text = "Post 1 is here").title,"Post 1")
    
    def test_delete_post(self):
        p2 = Post.objects.get(title="Post 2")
        p2.delete()
        self.assertFalse(Post.objects.filter(title="Post 2").exists())
        self.assertEqual(len(Post.objects.all()),1)

class CommentTest(TestCase):
    def setUp(self):
        Post.objects.create(title="Post 1", text="This is post 1", image=None, privacy=1, contentType=1)
        Post.objects.create(title="Post 2", text="This is post 2", image=None, privacy=1, contentType=0)

    def test_comment(self):
        p1 = Post.objects.get(title="Post 1")
        com = Comment(post=p1, comment_body="hello")
        self.assertEqual(str(com), "Comment hello by None")

# Issues with tokens and Reverse for 'request_post' with keyword arguments        
'''
class GetAllPostsTest(TestCase):
    def setUp(self):
        Post.objects.create(title="Post 1", text="This is post 1", image=None, privacy=1, contentType=1)
        Post.objects.create(title="Post 2", text="This is post 2", image=None, privacy=1, contentType=0)
        Post.objects.create(title="Post 3", text="*This is post 3*", image=None, privacy=1, contentType=1)
        Post.objects.create(title="Post 4", text="*This is post 4*", image=None, privacy=1, contentType=0)

    def test_get_all(self):
        headers = {"Authorization": "Token 959ddf93ce016a02c887172d1a11bbeb697ccf80"}
        response = client.get(reverse('request_post_list'), headers=headers)
        all_post = Post.objects.all()
        serializer = PostSerializer(all_post, many=True)
        
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class getSinglePostsTest(TestCase):
    def setUp(self):
        self.p1 = Post.objects.create(title="Post 1", text="This is post 1", image=None, privacy=1, contentType=1)
        self.p2 = Post.objects.create(title="Post 2", text="This is post 2", image=None, privacy=1, contentType=0)
        self.p3 = Post.objects.create(title="Post 3", text="*This is post 3*", image=None, privacy=1, contentType=1)
        self.p4 = Post.objects.create(title="Post 4", text="*This is post 4*", image=None, privacy=1, contentType=0)

    def test_get_valid_one(self):
        headers = {"Authorization": "Token 959ddf93ce016a02c887172d1a11bbeb697ccf80"}
        print(self.p1)
        response = client.get(reverse('request_post', kwargs={'pk': self.p1.pk}))
        this_post = Post.objects.get(pk=self.p1.pk)
        serializer = PostSerializer(this_post, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
'''