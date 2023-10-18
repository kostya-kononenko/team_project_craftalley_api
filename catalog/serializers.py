from rest_framework import serializers

from catalog.models import Catalog


class CatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalog
        fields = (
            "id",
            "name",
        )
