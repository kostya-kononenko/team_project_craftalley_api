from django.db import models
from product.models import Product, Category


class Campaign(models.Model):
    discount_type = models.CharField(
        max_length=6,
        choices=(("Amount", "amount"), ("Rate", "rate")),
        default="rate",
        null=False,
    )
    discount_rate = models.IntegerField(null=True, blank=True)
    discount_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    min_purchased_items = models.IntegerField(null=False)
    apply_to = models.CharField(
        max_length=8,
        choices=(("Product", "product"), ("Category", "category")),
        default="product",
        null=False,
    )
    target_product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=True
    )
    target_category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f"{self.discount_type} - "
            f"{self.discount_rate} - "
            f"{self.discount_amount} - "
            f"{self.min_purchased_items} - "
            f"{self.apply_to} - "
            f"{self.target_product} - "
            f"{self.target_category} - "
            f"{self.created_at} - "
            f"{self.updated_at}"
        )


class Coupon(models.Model):
    minimum_cart_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=False
    )
    discount_rate = models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f"{self.minimum_cart_amount} - "
            f"{self.discount_rate} - "
            f"{self.created_at} - "
            f"{self.updated_at}"
        )
