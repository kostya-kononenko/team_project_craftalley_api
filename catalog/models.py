from django.db import models


class Catalog(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]
        verbose_name = "catalog"
        verbose_name_plural = "catalogs"

    def __str__(self):
        return self.name
