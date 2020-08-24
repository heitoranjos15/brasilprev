# from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


User = get_user_model()


class UserTests(APITestCase):

    def test_can_create_user(self):
        url = reverse('register')
        data = {
            'username': 'bogus',
            'password': 'password123',
            'email': 'email@email.com',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg='{}'.format(response.data))
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'bogus')
