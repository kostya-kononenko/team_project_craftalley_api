from unittest import mock

from django.contrib.auth import get_user_model
from django.db import models
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from catalog.models import Catalog
from category.models import Category
from product.models import Product
from product.serializers import (
    ProductListSerializer)
from user.models import User

PRODUCT_URL = reverse("product:product-list")


def detail_url(product_id: int):
    return reverse("product:product-detail", args=[product_id])


def sample_product(**params):
    catalog = Catalog.objects.create(name="test catalog")
    category = Category.objects.create(
        name="test category",
        catalog=catalog
    )
    manufacturer = User.objects.create(email="test@test.com", password="test12345")

    defaults = {
        "name": "Test name",
        "description": "test description",
        "characteristics": "test characteristics",
        "delivery": "Ukrposhta",
        "return_conditions": "test return_conditions",
        "price": 10,
        "new_product": True,
        "coupon": "test coupon",
        "quantity": 5,
        "category": category,
        "manufacturer": manufacturer,
    }
    defaults.update(params)
    return Product.objects.create(**defaults)


class AuthenticatedProductApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "user@user.com",
            "user12345",
        )
        self.client.force_authenticate(self.user)

    def test_create_product_success(self):
        catalog = Catalog.objects.create(name="test catalog")
        category = Category.objects.create(
            name="test category",
            catalog=catalog
        )
        manufacturer = User.objects.create(email="test@test.com", password="test12345")
        payload = {
            "name": "Test name",
            "description": "test description",
            "characteristics": "test characteristics",
            "delivery": "ukrposhta",
            "return_conditions": "test return_conditions",
            "price": 10,
            "new_product": True,
            "coupon": "test_coup",
            "quantity": 5,
            "category": category.id,
            "manufacturer": manufacturer.id,
        }
        res = self.client.post(PRODUCT_URL, payload)
        print(res.json())
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    @mock.patch("product.check_ip_for_rating.get_client_ip")
    def test_list_product(self, mock_get_client_ip):
        mock_get_client_ip.return_value = "127.1.1.1."
        sample_product()
        res = self.client.get(
           PRODUCT_URL,
        )
        product = (
            Product.objects.all()
            .annotate(
                rating_user=models.Count(
                    "ratings", filter=models.Q(ratings__ip=mock_get_client_ip())
                )
            )
            .annotate(
                middle_star=models.Sum(models.F("ratings__star"))
                / models.Count(models.F("ratings"))
            )
        )
        serializer = ProductListSerializer(product, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_retrieve_product_detail(self):
        product = sample_product()
        url = detail_url(product.id)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_update_product_success(self):
        product = sample_product()
        payload = {
            "name": "New name",
        }
        url = detail_url(product.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_product_success(self):
        product = sample_product()
        url = detail_url(product.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)


class AdminAirplaneApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com", "admin12345", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_product_success(self):
        catalog = Catalog.objects.create(name="test catalog")
        category = Category.objects.create(
            name="test category",
            catalog=catalog
        )
        manufacturer = User.objects.create(email="test@test.com", password="test12345")
        payload = {
            "name": "Test name",
            "description": "test description",
            "characteristics": "test characteristics",
            "delivery": "ukrposhta",
            "return_conditions": "test return_conditions",
            "price": 10,
            "new_product": True,
            "coupon": "test_coup",
            "quantity": 5,
            "category": category.id,
            "manufacturer": manufacturer.id,
        }
        res = self.client.post(PRODUCT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_update_product_success(self):
        product = sample_product()
        payload = {
            "name": "New name",
        }
        url = detail_url(product.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_airplane_success(self):
        product = sample_product()
        url = detail_url(product.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
