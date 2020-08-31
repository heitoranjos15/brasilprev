# from django.test import TestCase
import base64
import json
from random import randrange

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Product

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
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            msg='{}'.format(response.data)
        )
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'bogus')


class ProductTests(APITestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser('admin', 'admin@email.com', '123456')
        self.user = User(username='bogus', email='bogus@email.com')
        self.user.set_password('123456')
        self.user.save()
        self.url = reverse('product-list')
        self.payload = {
            'name': 'test',
            'width': 50,
            'depth': 10,
            'height': 20,
            'weight': 30,
            'price': 150.50,
        }

    def test_can_admin_add_product(self):
        auth = base64.b64encode('admin:123456'.encode()).decode()
        header_data = {
            'HTTP_AUTHORIZATION': 'Basic ' + auth,
        }
        response = self.client.post(
            self.url,
            json.dumps(self.payload),
            content_type="application/json",
            **header_data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            msg='{}'.format(response.data)
        )

    def test_can_client_add_product(self):
        auth = base64.b64encode('bogus:123456'.encode()).decode()
        header_data = {
            'HTTP_AUTHORIZATION': 'Basic ' + auth,
        }
        response = self.client.post(
            self.url,
            json.dumps(self.payload),
            content_type="application/json",
            **header_data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
            msg='{}'.format(response.data)
        )

    def test_can_add_product_without_authentication(self):
        response = self.client.post(
            self.url,
            json.dumps(self.payload),
            content_type="application/json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            msg='{}'.format(response.data)
        )


class OrderTest(APITestCase):
    def setUp(self):
        self.user = User(username='bogus', email='bogus@email.com')
        self.user.set_password('123456')
        self.user.save()
        self.url = reverse('order')
        for i in range(4):
            product = Product(
                name='item-{}'.format(i),
                width=randrange(10, 100),
                depth=randrange(10, 100),
                height=randrange(20, 100),
                weight=randrange(30, 200),
                price=randrange(50, 200)
            )
            product.save()
        self.payload = {
            'products': [
                {
                    'product_id': 3,
                    'product_quantity': 7,
                },
                {
                    'product_id': 2,
                    'product_quantity': 8
                }
            ]
        }

    def test_user_can_order_products(self):
        auth = base64.b64encode('bogus:123456'.encode()).decode()
        header_data = {
            'HTTP_AUTHORIZATION': 'Basic ' + auth,
        }
        response = self.client.post(
            self.url,
            json.dumps(self.payload),
            content_type="application/json",
            **header_data
            )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_can_order_products_without_authentication(self):
        response = self.client.post(self.url, self.payload)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            msg='{}'.format(response.data)
        )
