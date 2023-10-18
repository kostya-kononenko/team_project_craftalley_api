from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from cart.models import Cart
from catalog.models import Catalog
from category.models import Category
from product.models import Product
from user.models import User


class CartTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user("user@user.com", "user12345")
        self.client.force_authenticate(self.user)

    def test_create_cart_item(self):
        catalog = Catalog.objects.create(name="test catalog")

        self.test_user = User.objects.create(email='test@test.ua', password="test12345")
        self.test_category = Category.objects.create(name='Test Category',
                                                     catalog=catalog)

        self.test_product = Product.objects.create(category=self.test_category,
                                                   name='Test Product',
                                                   price=10,
                                                   quantity=5,
                                                   manufacturer=self.test_user,)
        data = {'user': self.test_user.id,
                'item': self.test_product.id,
                'quantity': 1}
        response = self.client.post('/cart/cart/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cart.objects.count(), 1)
        self.assertEqual(Cart.objects.get().item.name, self.test_product.name)

    def test_checkout_by_user(self):
        catalog = Catalog.objects.create(name="test catalog")

        self.test_user = User.objects.create(email='test@test.ua', password="test12345")
        self.test_category = Category.objects.create(name='Test Category 3',
                                                     catalog=catalog)

        self.test_product = Product.objects.create(category=self.test_category,
                                                   name='Test Product',
                                                   price=10,
                                                   quantity=5,
                                                   manufacturer=self.test_user,)

        self.test_cart_item = Cart.objects.create(user=self.test_user,
                                                  item=self.test_product,
                                                  quantity=4)

        response = self.client.get("/cart/cart/checkout/{0}/".format(self.test_user.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data.get('checkout_details', False).get('products', False), False)
        self.assertNotEqual(response.data.get('checkout_details', False).get('total', False), False)
        self.assertNotEqual(response.data.get('checkout_details', False).get('amount', False), False)
