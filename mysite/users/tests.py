from django.forms.fields import EmailField
from django.test import TestCase
from django.urls import reverse
from django.test.utils import setup_test_environment
from django.contrib.auth import authenticate
from django.test import Client
from .models import Create_user, User, User_Profile, UserFollows, FriendRequest, Post
import datetime

# Create your tests here.
client = Client()

#friend request testing
class FriendRequestModelTests(TestCase):
    user1 = User(username="user1", password="1")
    user1_profile = User_Profile(user=user1)
    user2= User(username="user2", password='2')
    user2_profile = User_Profile(user=user2)


    def test_create_friend_request(self):
        f_req = FriendRequest(actor=self.user1_profile, object=self.user2_profile)
        self.assertIs(f_req.actor == self.user1_profile, True)
        self.assertIs(f_req.object == self.user2_profile, True)



#following testing
class UserFollowsModelsTests(TestCase):
    user1 = User(username="user1", password="1")
    user1_profile = User_Profile(user=user1)
    user2= User(username="user2", password='2')
    user2_profile = User_Profile(user=user2)

    def test_create_user_follow(self):
        user_follow = UserFollows(actor=self.user1_profile, object=self.user2_profile)
        self.assertIs(user_follow.actor == self.user1_profile, True)
        self.assertIs(user_follow.object == self.user2_profile, True)


#checking for users test
class UserViewsTests(TestCase):
    user1 = User(username="user1", password="1", id=1)
    user1_profile = User_Profile(user=user1)
    
    def test_homepage(self):
        response = self.client.get(reverse('users:homepage'))
        self.assertTrue(response.status_code != 404)


    def test_wrong_view_request(self):
        response = self.client.get(reverse('users:view_requests', args=([100])))
        self.assertEqual(response.status_code, 403)



class UserProfileTests(TestCase):
    user1 = User(username="user1", password="1", id=1)
    user1_profile = User_Profile(user=user1)
        
    def test_user_profile(self):
        user_profile = User_Profile.objects.filter(user_id = self.user.id)[0]
        user_profile.firstName=datetime.date('Test') 
        user_profile.save()
        self.assertEqual(User_Profile.objects.filter(user_id=self.user.id).values_list('firstName', flat=True)[0],)



class PostModelTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='test', password='hello')
		self.second_user = User.objects.create_user(username='test2', password='hello')
		self.user.save()
		self.second_user.save()
		login = self.client.login(username='test', password='hello')
		self.posts_to_delete = []
		self.post = Post.objects.create(author=self.user,
		title="Test Title", description="This is a test Post", published=datetime.datetime.now(), content="TESTING",
		images=None)
		self.new_post.save()

	def delete(self):
		User.objects.filter(username = self.user).delete()
		self.post.delete()
		for post in self.delete_post:
				Post.objects.filter(id=post).delete()


	def addingPosts(self):
		# posting 
		existing_ID = Post.objects.filter(title="Test").values_list('id', flat=True)
		
		totalID = len(existing_ID)
		response = self.client.post("/post/",data={"author":self.user.id, "contentType":"text/plain",
		"title":"Test", "description":"Testing",
		"visibility":"PUBLIC", "published":datetime.datetime.now(), "content":"TEST POST 2"})
		id_to_delete = ""

		addedPost = Post.objects.filter(title="Test Title").values_list('id', flat=True)
		self.assertEqual(len(addedPost), totalID + 1)
		for id_val in list(addedPost):
				if id_val not in list(existing_ID):
						id_to_delete = id_val
						self.posts_to_delete.append(id_to_delete)

		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, "/author/"+ str(self.user.username) + "/posts/" + str(id_to_delete))

	def test_editingPosts(self):
		# Editing post and checking if post is edited
		response = self.client.post("/author/"+ str(self.user.id) + "/posts/" + str(self.new_post.id) + "/edit",data={'author': ['1'], "contentType":["text/markdown"],
		"title":["Test Title"], "description":["This is a test Post"],
		"visibility":["PUBLIC"], "content":["TEST POST(EDITED)"],
		"images":[""], "originalPost":[""], "sharedBy":[""]})

		editedPost = Post.objects.filter(id=self.new_post.id)
		self.assertEqual(editedPost[0].content, "TEST POST(EDITED)")

	def test_deletingPosts(self):
		# Deleting post and checking if post is deleted
		oldPost = Post.objects.filter(id=self.new_post.id)
		self.assertEqual(len(oldPost), 1)
		response = self.client.post("/author/"+ str(self.user.id) + "/posts/" + str(self.new_post.id) + "/delete")

		oldPost = Post.objects.filter(id=self.new_post.id)
		self.assertEqual(len(oldPost), 0)

	def test_sharingPosts(self):
		# Sharing post and checking if post is shared
		totalShare = Post.objects.filter(originalPost=self.new_post)
		totalShares = len(totalShare)
		response = self.client.get("/author/"+ str(self.user.id) + "/posts/" + str(self.new_post.id) + "/share")

		totalShare = Post.objects.filter(originalPost=self.new_post)
		self.assertEqual(len(totalShare), totalShares + 1)

	def test_restrictions(self):
		other_post = Post.objects.create(author=self.other_user,
		title="Test Title", description="This is a test Post", published=datetime.datetime.now(), content="TEST POST 1",
		images=None, originalPost=None, sharedBy=None)
		other_post.save()

		response = self.client.get("/"+self.other_user.username + "/posts/" + str(other_post.id))

		# Checking For unauthorized access
		# response_str = str(response.rendered_content)
		response_str = str(response.content)
		self.assertEqual("Edit" in response_str, False)
		self.assertEqual("Delete" in response_str, False)

		login = self.client.login(username='testuser2', password='12345')
		response = self.client.get("/author/"+ str(self.other_user.id) + "/posts/" + str(other_post.id))

		# Checking for authorized access
		response_str = str(response.content)
		self.assertEqual("Edit" in response_str, True)
		self.assertEqual("Delete" in response_str, True)


class CommentTests(TestCase):
   def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.user.save()
        login = self.client.login(username='testuser', password='12345')
        self.new_post = Post.objects.create(author=self.user,
		title="Test Title", description="This is a test Post", published=datetime.datetime.now(), content="TEST POST 1",
		images=None, originalPost=None, sharedBy=None)
        self.new_post.save()
        
   def test_comments(self):
   	comment = Comment.objects.create(author=self.user,post=self.new_post,comment='test comment' )
   	comment.save()
   	self.assertEqual(len(Comment.objects.filter(author=self.user).values_list('id', flat=True)),1)
   	
