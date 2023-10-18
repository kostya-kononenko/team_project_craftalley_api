from rest_framework import serializers

from category.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "catalog",
        )


class CategoryListSerializer(serializers.ModelSerializer):
    catalog = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="name"
    )

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "catalog",
        )


class CategoryDetailSerializer(serializers.ModelSerializer):
    catalog = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="name"
    )

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "catalog",
        )
