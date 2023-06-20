from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

# Create your tests here.
class TestUserAuthentication(TestCase):
    def setUp(self):
        self.UserModel = get_user_model()
        self.test_username = 'cs350user'
        self.test_password = 'cs350password'
        self.test_email = 'cs350user@kaist.ac.kr'
        self.test_user = self.UserModel.objects.create_user(self.test_username, self.test_email, self.test_password)

    def test_authenticate_valid_user(self):
        logged_in = self.client.login(username=self.test_username, password=self.test_password)
        self.assertTrue(logged_in, 'User with correct credentials should be able to log in.')

    def test_authenticate_invalid_user(self):
        logged_in = self.client.login(username=self.test_username, password='invalid_password')
        self.assertFalse(logged_in, 'User with incorrect password should not be able to log in.')


class TestUserSession(TestCase):
    def setUp(self):
        self.UserModel = get_user_model()
        self.test_username = 'cs350user'
        self.test_password = 'cs350password'
        self.test_email = 'cs350user@kaist.ac.kr'
        self.test_user = self.UserModel.objects.create_user(self.test_username, self.test_email, self.test_password)
        # self.protected_url = reverse('user_account:protected')

    def test_full_user_session(self):
        # Test login
        logged_in = self.client.login(username=self.test_username, password=self.test_password)
        self.assertTrue(logged_in, 'User with correct credentials should be able to log in.')

        # Test accessing a protected view
        # response = self.client.get(self.protected_url)
        # self.assertEqual(response.status_code, 200, 'Authenticated user should be able to access protected views.')

        # Test logout
        self.client.logout()
        
        # Test accessing the protected view again after logout
        # response = self.client.get(self.protected_url)
        # self.assertNotEqual(response.status_code, 200, 'Logged out user should not be able to access protected views.')
