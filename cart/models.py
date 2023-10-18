from django.db import models
from product.models import Product


class Cart(models.Model):
    user = models.ForeignKey("user.User", on_delete=models.SET_NULL, null=True, blank=True)
    item = models.ForeignKey("product.Product", on_delete=models.SET_NULL, null=True, blank=True, related_name="carts")
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status_item = models.BooleanField(default=True)

    def __str__(self):
        return (
            f"{self.user} - "
            f"{self.item} - "
            f"{self.quantity} - "
            f"{self.created_at} - "
            f"{self.updated_at}"
        )
