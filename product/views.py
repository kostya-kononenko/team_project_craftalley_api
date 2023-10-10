from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django.db import models


from product.check_ip_for_rating import get_client_ip
from product.models import Catalog, Category, Product, Rating
from product.serializers import CatalogSerializer, CategorySerializer, CategoryListSerializer, CategoryDetailSerializer, \
    ProductSerializer, ProductListSerializer, ProductDetailSerializer, CreateRatingSerializer


class CatalogPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 100


class CatalogViewSet(viewsets.ModelViewSet):
    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer
    pagination_class = CatalogPagination


class CategoryPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 100


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    pagination_class = CategoryPagination

    def get_serializer_class(self):
        if self.action == "list":
            return CategoryListSerializer
        if self.action == "retrieve":
            return CategoryDetailSerializer
        return CategorySerializer


class ProductPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    pagination_class = ProductPagination

    def get_queryset(self):
        product = (
            Product.objects.all()
            .annotate(
                rating_user=models.Count(
                    "ratings", filter=models.Q(
                        ratings__ip=get_client_ip(self.request))
                )
            )
            .annotate(
                middle_star=models.Sum(models.F("ratings__star"))
                            / models.Count(models.F("ratings"))
            )
        )
        return product

    def get_serializer_class(self):
        if self.action == "list":
            return ProductListSerializer
        if self.action == "retrieve":
            return ProductDetailSerializer
        return ProductSerializer


class AddStarRatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))
