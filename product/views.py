from rest_framework import viewsets
from django.db import models
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from product.check_ip_for_rating import get_client_ip
from product.models import Product, Rating
from product.pagination import ProductPagination
from product.serializers import (
    ProductSerializer,
    ProductListSerializer,
    ProductDetailSerializer,
    CreateRatingSerializer,
)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    pagination_class = ProductPagination
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def perform_create(self, serializer):
        serializer.save(manufacturer=self.request.user)

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


class AddProductStarRatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = CreateRatingSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))
