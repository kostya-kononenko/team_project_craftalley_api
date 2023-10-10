from rest_framework import serializers

from product.models import Catalog, Category, Product, Rating
from user.serializers import UserDetailSerializer


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
    middle_star = serializers.IntegerField()
    rating_user = serializers.BooleanField()

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
            "middle_star",
            "rating_user",
        )


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategoryDetailSerializer(many=False)
    manufacturer = UserDetailSerializer(many=False)
    middle_star = serializers.IntegerField()
    rating_user = serializers.BooleanField()

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
            "middle_star",
            "rating_user",
        )


class CreateRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ("star", "product", "ip")

        def create(self, validate_data):
            rating = Rating.objects.update_or_create(
                ip=validate_data.get("ip", None),
                product=validate_data.get("product", None),
                defaults={"star": validate_data.get("star")},
            )
            return rating
