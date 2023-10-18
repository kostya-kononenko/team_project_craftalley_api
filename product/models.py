from django.db import models

class Product(models.Model):
    class Delivery(models.TextChoices):
        Ukrposhta = "ukrposhta", "ukrposhta"
        Novaposhta = "novaposhta", "novaposhta"
        Сourier = "courier", "courier"
        Pickup = "pickup", "pickup"

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    characteristics = models.TextField(blank=True)
    delivery = models.CharField(
        max_length=25, choices=Delivery.choices, default=Delivery.Novaposhta
    )
    return_conditions = models.TextField(blank=True)
    price = models.DecimalField(null=True, max_digits=10, decimal_places=2)
    new_product = models.BooleanField(default=True)
    coupon = models.CharField(max_length=10, blank=True)
    quantity = models.IntegerField()
    category = models.ForeignKey(
        "category.Category", related_name="products", on_delete=models.CASCADE
    )
    manufacturer = models.ForeignKey("user.User",
                                     on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True,
                              upload_to="images/products/")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(
                fields=[
                    "id",
                ]
            ),
            models.Index(fields=["name"]),
            models.Index(fields=["-created"]),
        ]

    def __str__(self):
        return self.name


class RatingStarProduct(models.Model):
    value = models.PositiveSmallIntegerField("Meaning", default=0)

    def __str__(self):
        return f"{self.value}"

    class Meta:
        verbose_name = "Star rating"
        verbose_name_plural = "Rating Stars"
        ordering = ["-value"]


class Rating(models.Model):
    ip = models.CharField("IP address", max_length=15)
    star = models.ForeignKey(
        RatingStarProduct, on_delete=models.CASCADE, verbose_name="star"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="ratings"
    )

    def __str__(self):
        return f"{self.star} - {self.product}"

    class Meta:
        verbose_name = "Rating"
        verbose_name_plural = "Ratings"
