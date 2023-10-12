from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from product.models import Catalog
from product.serializers import CatalogSerializer

CATALOG_URL = reverse("product:catalog-list")


def detail_url(catalog_id: int):
    return reverse("product:catalog-detail", args=[catalog_id])


def sample_catalog(**params):
    defaults = {
        "name": "Test Catalog",
    }

    defaults.update(params)
    return Catalog.objects.create(**defaults)


class UnauthenticatedCatalogApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(CATALOG_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedCatalogApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user("user@user.com", "user12345")
        self.client.force_authenticate(self.user)

    def test_list_catalog(self):
        sample_catalog()
        res = self.client.get(CATALOG_URL, )
        catalog = Catalog.objects.all()
        serializer = CatalogSerializer(catalog, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)

    def test_retrieve_catalog_detail(self):
        catalog = sample_catalog()
        url = detail_url(catalog.id)
        res = self.client.get(url)
        serializer = CatalogSerializer(catalog)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_category_forbidden(self):
        payload = {
            "name": "Test New Name",
        }
        res = self.client.post(CATALOG_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_category_forbidden(self):
        catalog = sample_catalog()
        payload = {
            "name": "Test New Name 2",
        }
        url = detail_url(catalog.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_category_forbidden(self):
        catalog = sample_catalog()
        url = detail_url(catalog.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminCategoryApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com", "admin12345", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_catalog_success(self):
        payload = {
            "name": "Test Very New Name",
        }
        res = self.client.post(CATALOG_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_update_catalog_success(self):
        catalog = sample_catalog()
        payload = {
            "name": "New Name 3",
        }
        url = detail_url(catalog.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_catalog_success(self):
        catalog = sample_catalog()
        url = detail_url(catalog.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
