from django.db import models


class Discount(models.Model):
    name = models.CharField(max_length=20)
    discount = models.DecimalField(null=True, max_digits=10, decimal_places=2)

    def __str__(self):
        return (
            f"{self.name} - "
            f"{self.discount} - "
        )
