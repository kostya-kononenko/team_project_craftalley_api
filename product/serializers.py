from rest_framework import serializers

from category.serializers import CategoryDetailSerializer
from comment.serializers import CommentDetailSerializer
from product.models import Product, Rating, FavoriteProduct
from user.serializers import UserDetailSerializer


class ProductSerializer(serializers.ModelSerializer):
    middle_star = serializers.IntegerField(read_only=True)
    rating_user = serializers.BooleanField(read_only=True)

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
            "image",
            "created",
            "updated",
            "middle_star",
            "rating_user"
        )


class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="name"
    )
    manufacturer = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="brand_name"
    )
    middle_star = serializers.IntegerField(read_only=True)
    rating_user = serializers.BooleanField(read_only=True)

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
    middle_star = serializers.IntegerField(read_only=True)
    rating_user = serializers.BooleanField(read_only=True)
    comments = CommentDetailSerializer(many=True, read_only=True)

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
            "comments",
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


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteProduct
        fields = (
            "id",
            "user",
            "product",
        )

    def validate(self, data):
        favorite = FavoriteProduct.objects.filter(
            product_id=data["product"], user_id=data["user"]
        )
        if favorite:
            raise serializers.ValidationError(
                "You had already add this product to favorite")
        return data


class FavoriteDetailSerializer(serializers.ModelSerializer):
    first_name = serializers.ReadOnlyField(source="user.first_name")
    last_name = serializers.ReadOnlyField(source="user.last_name")

    class Meta:
        model = FavoriteProduct
        fields = (
            "id",
            "first_name",
            "last_name")
