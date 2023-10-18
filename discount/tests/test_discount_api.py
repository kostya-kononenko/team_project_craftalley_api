from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from discount.models import Discount

DISCOUNT_URL = reverse("discount:discount-list")


def detail_url(discount_id: int):
    return reverse("discount:discount-detail", args=[discount_id])


def sample_discount(**params):
    defaults = {
        "name": "Test Discount",
    }

    defaults.update(params)
    return Discount.objects.create(**defaults)


class UnauthenticatedDiscountApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(DISCOUNT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedDiscountApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "user@user.com",
            "user12345",
        )
        self.client.force_authenticate(self.user)

    def test_list_discount_forbidden(self):
        sample_discount()
        res = self.client.get(DISCOUNT_URL,)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_discount_forbidden(self):
        payload = {
            "name": "Sample airplane type",
        }
        res = self.client.post(DISCOUNT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_discount_forbidden(self):
        discount = sample_discount()
        payload = {
            "name": "New name",
        }
        url = detail_url(discount.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_discount_forbidden(self):
        discount = sample_discount()
        url = detail_url(discount.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminDiscountApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com",
            "admin12345",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_discount_success(self):
        payload = {
            "name": "New discount",
        }
        res = self.client.post(DISCOUNT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_update_discount_success(self):
        discount = sample_discount()
        payload = {
            "name": "New name",
        }
        url = detail_url(discount.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_discount_success(self):
        discount = sample_discount()
        url = detail_url(discount.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)