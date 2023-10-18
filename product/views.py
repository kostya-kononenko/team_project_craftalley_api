from rest_framework import viewsets
from django.db import models
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets, status

from product.calculate_all_favorite_product import FavoriteHelper
from product.check_ip_for_rating import get_client_ip
from product.models import Product, Rating, FavoriteProduct
from rest_framework.exceptions import ValidationError
from product.pagination import ProductPagination
from product.serializers import (
    ProductSerializer,
    ProductListSerializer,
    ProductDetailSerializer,
    CreateRatingSerializer,
    FavoriteSerializer,
)
from user.models import User


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
        if self.action == "add_favorite":
            return FavoriteSerializer
        return ProductSerializer

    @action(detail=True, methods=["POST"], url_path="favorite")
    def add_favorite(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        user = request.user
        serializer = FavoriteSerializer(data={"product": product.id, "user": user.id})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_serializer = ProductDetailSerializer(product)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["POST"], url_path="remove_favorite")
    def remove_favorite(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        user = request.user
        favorite = FavoriteProduct.objects.filter(product__id=product.id, user__id=user.id)
        if not favorite:
            raise ValidationError("You hadn't add this product to favorite yet")
        favorite.delete()
        response_serializer = ProductDetailSerializer(product)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False, url_path="checkout_favorite/(?P<userId>[^/.]+)", url_name="checkout_favorite", )
    def checkout(self, request, *args, **kwargs):
        try:
            user = User.objects.get(pk=int(kwargs.get("userId")))
        except Exception as e:
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={"Error": str(e)})

        favorite_helper = FavoriteHelper(user)
        checkout_details = favorite_helper.prepare_favorite_for_checkout()

        if not checkout_details:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"error": "You haven't added any products to your favorites yet"},
            )

        return Response(
            status=status.HTTP_200_OK, data={
                "checkout_details": checkout_details}
        )


class AddProductStarRatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = CreateRatingSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))
