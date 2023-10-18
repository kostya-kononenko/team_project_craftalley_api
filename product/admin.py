from django.contrib import admin
from .models import Product, Rating, RatingStarProduct


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


admin.site.register(RatingStarProduct)
