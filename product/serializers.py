from rest_framework import serializers

from product.models import Catalog, Category, Product
from user.serializers import UserSerializer, UserDetailSerializer


class CatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalog
        fields = (
            "id",
            "name",
        )


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
        many=False, read_only=True, slug_field="name")

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "catalog",
        )


class CategoryDetailSerializer(serializers.ModelSerializer):
    catalog = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="name")

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "catalog",
        )


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "description",
            "characteristics",
            "delivery",
            "return_conditions",
            "price",
            "new_product",
            "coupon",
            "quantity",
            "category",
            "manufacturer",
            "image",
            "created",
            "updated",
        )


class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="name")
    manufacturer = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="brand_name")

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "description",
            "characteristics",
            "delivery",
            "return_conditions",
            "price",
            "new_product",
            "coupon",
            "quantity",
            "category",
            "manufacturer",
            "image",
            "created",
            "updated",
        )


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategoryDetailSerializer(many=False)
    manufacturer = UserDetailSerializer(many=False)

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "description",
            "characteristics",
            "delivery",
            "return_conditions",
            "price",
            "new_product",
            "coupon",
            "quantity",
            "category",
            "manufacturer",
            "image",
            "created",
            "updated",
        )