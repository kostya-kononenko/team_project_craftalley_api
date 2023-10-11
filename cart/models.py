from django.db import models
from product.models import Product


class Cart(models.Model):
    user = models.ForeignKey(
        "user.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    item = models.ForeignKey(Product,
                             on_delete=models.SET_NULL,
                             null=True,
                             blank=True)
    quantity = models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f"{self.user} - "
            f"{self.item} - "
            f"{self.quantity} - "
            f"{self.created_at} - "
            f"{self.updated_at}"
        )


class DeliveryCost(models.Model):
    status = models.CharField(
        max_length=7,
        choices=(("Active", "active"), ("Passive", "passive")),
        default="passive",
        null=False,
    )
    cost_per_delivery = models.DecimalField(max_digits=10,
                                            decimal_places=2,
                                            null=False)
    cost_per_product = models.DecimalField(max_digits=10,
                                           decimal_places=2,
                                           null=False)
    fixed_cost = models.DecimalField(max_digits=10,
                                     decimal_places=2,
                                     null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f"{self.status} - "
            f"{self.cost_per_delivery} - "
            f"{self.cost_per_product} - "
            f"{self.fixed_cost} - "
            f"{self.created_at} - "
            f"{self.updated_at}"
        )
