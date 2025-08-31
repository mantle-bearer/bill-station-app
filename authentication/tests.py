from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.cache import cache
from rest_framework.test import APITestCase
from rest_framework import status

User = get_user_model()

class UserRegistrationTestCase(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.valid_payload = {
            'email': 'test@example.com',
            'full_name': 'Test User',
            'password': 'StrongPassword123!',
            'password_confirm': 'StrongPassword123!'
        }

    def test_user_registration_success(self):
        response = self.client.post(self.register_url, self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='test@example.com').exists())
        self.assertIn('tokens', response.data)

    def test_user_registration_password_mismatch(self):
        payload = self.valid_payload.copy()
        payload['password_confirm'] = 'DifferentPassword123!'
        response = self.client.post(self.register_url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_duplicate_email(self):
        User.objects.create_user(
            username='test@example.com',
            email='test@example.com',
            full_name='Existing User',
            password='password123'
        )
        response = self.client.post(self.register_url, self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UserLoginTestCase(APITestCase):
    def setUp(self):
        self.login_url = reverse('login')
        self.user = User.objects.create_user(
            username='test@example.com',
            email='test@example.com',
            full_name='Test User',
            password='TestPassword123!'
        )

    def test_user_login_success(self):
        payload = {
            'email': 'test@example.com',
            'password': 'TestPassword123!'
        }
        response = self.client.post(self.login_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('tokens', response.data)

    def test_user_login_invalid_credentials(self):
        payload = {
            'email': 'test@example.com',
            'password': 'WrongPassword'
        }
        response = self.client.post(self.login_url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class PasswordResetTestCase(APITestCase):
    def setUp(self):
        self.forgot_password_url = reverse('forgot_password')
        self.reset_password_url = reverse('reset_password')
        self.user = User.objects.create_user(
            username='test@example.com',
            email='test@example.com',
            full_name='Test User',
            password='TestPassword123!'
        )

    def test_forgot_password_success(self):
        payload = {'email': 'test@example.com'}
        response = self.client.post(self.forgot_password_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('reset_token', response.data)

    def test_forgot_password_user_not_found(self):
        payload = {'email': 'nonexistent@example.com'}
        response = self.client.post(self.forgot_password_url, payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_reset_password_success(self):
        # First, get a reset token
        forgot_response = self.client.post(
            self.forgot_password_url, 
            {'email': 'test@example.com'}
        )
        reset_token = forgot_response.data['reset_token']
        
        # Then use it to reset password
        payload = {
            'token': reset_token,
            'new_password': 'NewStrongPassword123!',
            'confirm_password': 'NewStrongPassword123!'
        }
        response = self.client.post(self.reset_password_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
