from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from interface.models import Organization

User = get_user_model()

class RegisterViewTests(APITestCase):

    def setUp(self):
        self.url = reverse('register')  # Update this to match your URL name
        self.valid_payload = {
            'email': 'testuser@example.com',
            'password': 'TestPass123!',
            'firstName': 'Test',
            'lastName': 'User',
            'phone': '1234567890'
        }
        self.invalid_payload = {
            'email': 'testuser@example.com',
            'password': 'short',
            'firstName': 'Test',
            'lastName': 'User',
            'phone': '1234567890'
        }

    def test_register_success(self):
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'success')
        self.assertIn('accessToken', response.data['data'])
        self.assertIn('refreshToken', response.data['data'])

        user = User.objects.get(email=self.valid_payload['email'])
        self.assertIsNotNone(user)
        self.assertTrue(user.check_password(self.valid_payload['password']))

    def test_register_failure_invalid_data(self):
        response = self.client.post(self.url, self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'Bad request')
        self.assertEqual(response.data['message'], 'Registration unsuccessful')
        self.assertEqual(response.data['statusCode'], 400)

    def test_user_assigned_to_default_organization(self):
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(email=self.valid_payload['email'])
        self.assertIsNotNone(user.organization)
        self.assertEqual(user.organization.name, "Your Default Organization")
