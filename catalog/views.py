from rest_framework import viewsets
from catalog.models import Catalog
from catalog.pagination import CatalogPagination
from catalog.permissions import IsAdminOrIfAnonymousReadOnly
from catalog.serializers import CatalogSerializer


class CatalogViewSet(viewsets.ModelViewSet):
    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer
    pagination_class = CatalogPagination
    permission_classes = (IsAdminOrIfAnonymousReadOnly,)
