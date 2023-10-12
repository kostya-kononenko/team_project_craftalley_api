from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from product.models import Category, Catalog
from product.serializers import CategoryListSerializer, CategoryDetailSerializer

CATEGORY_URL = reverse("product:category-list")


def detail_url(category_id: int):
    return reverse("product:category-detail", args=[category_id])


def sample_category(**params):
    catalog = Catalog.objects.create(name="test catalog")

    defaults = {
        "name": "Test Category",
        "catalog": catalog,
    }

    defaults.update(params)
    return Category.objects.create(**defaults)


class UnauthenticatedCategoryApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(CATEGORY_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedCategoryApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user("user@user.com", "user12345")
        self.client.force_authenticate(self.user)

    def test_list_category(self):
        sample_category()
        res = self.client.get(CATEGORY_URL, )
        category = Category.objects.all()
        serializer = CategoryListSerializer(category, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['results'], serializer.data)

    def test_retrieve_category_detail(self):
        category = sample_category()
        url = detail_url(category.id)
        res = self.client.get(url)
        serializer = CategoryDetailSerializer(category)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_category_forbidden(self):
        payload = {
            "name": "Test New Name",
        }
        res = self.client.post(CATEGORY_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_category_forbidden(self):
        category = sample_category()
        payload = {
            "name": "Test New Name 2",
        }
        url = detail_url(category.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_category_forbidden(self):
        category = sample_category()
        url = detail_url(category.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminCategoryApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com", "admin12345", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_category_success(self):
        catalog = Catalog.objects.create(name="Airplane555")
        payload = {
            "name": "Test Very New Name",
            "catalog": catalog.id
        }
        res = self.client.post(CATEGORY_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_update_category_success(self):
        category = sample_category()
        catalog = Catalog.objects.create(name="Airplane555")
        payload = {
            "name": "Test Very New Name",
            "catalog": catalog.id
        }
        url = detail_url(category.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_category_success(self):
        category = sample_category()
        url = detail_url(category.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
