from rest_framework import viewsets
from category.models import Category
from category.pagination import CategoryPagination
from category.permissions import IsAdminOrIfAnonymousReadOnly
from category.serializers import (
    CategorySerializer,
    CategoryListSerializer,
    CategoryDetailSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    pagination_class = CategoryPagination
    permission_classes = (IsAdminOrIfAnonymousReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return CategoryListSerializer
        if self.action == "retrieve":
            return CategoryDetailSerializer
        return CategorySerializer
