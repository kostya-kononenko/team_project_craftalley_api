from rest_framework import serializers

from product.models import Catalog, Category


class CatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalog
        fields = (
            "id",
            "name",
        )


class CategorySerializer(serializers.ModelSerializer):
    catalog = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="name")

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "catalog",
        )
