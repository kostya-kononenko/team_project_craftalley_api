from django.contrib import admin
from .models import (
    Product,
    Rating,
    RatingStarProduct,
    FavoriteProduct
)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "manufacturer",
        "price",
        "created",
        "updated",
    ]
    list_filter = ["created", "updated"]


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("id", "star", "product")


@admin.register(FavoriteProduct)
class FavoriteProductAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "product",
    ]
    search_fields = ("user",)
    list_filter = ("user",)


admin.site.register(RatingStarProduct)
