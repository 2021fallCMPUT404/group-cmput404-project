from django.test import TestCase
from django.contrib.auth.models import User
from users.models import User_Profile


class AnimalTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='testcase',
                                   first_name='test',
                                   last_name='case',
                                   email='testcase@ualberta.ca')
        User_Profile.objects.create(
            displayName='case_1',
            profileImage='test_image.jpg',
            github='https://github.com/orgs/2021fallCMPUT404/dashboard',
            bio='test_bio')

    def test_users_model_displayName(self):
        """Animals that can speak are correctly identified"""
        test_user_1 = User.objects.get(name="testcase")
        test_profile_1 = User_Profile.objects.get(user=test_user_1)
        self.assertEqual(test_profile_1.__str__(), 'case_1')
