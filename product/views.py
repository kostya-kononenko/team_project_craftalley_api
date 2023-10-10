from rest_framework import viewsets

from product.models import Catalog, Category, Product
from product.serializers import CatalogSerializer, CategorySerializer, CategoryListSerializer, CategoryDetailSerializer, \
    ProductSerializer, ProductListSerializer, ProductDetailSerializer


class CatalogViewSet(viewsets.ModelViewSet):
    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return CategoryListSerializer
        if self.action == "retrieve":
            return CategoryDetailSerializer
        return CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return ProductListSerializer
        if self.action == "retrieve":
            return ProductDetailSerializer
        return ProductSerializer
