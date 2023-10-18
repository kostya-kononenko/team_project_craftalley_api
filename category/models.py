from django.db import models

from catalog.models import Catalog


class Category(models.Model):
    name = models.CharField(max_length=200)
    catalog = models.ForeignKey(
        Catalog, related_name="categories", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name
