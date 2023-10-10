import os
import uuid

from django.db import models
from django.utils.text import slugify


def comment_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads", "comment", filename)


class Comment(models.Model):
    content = models.TextField()
    image = models.ImageField(null=True, upload_to=comment_image_file_path)
    user = models.ForeignKey("user.User", on_delete=models.SET_NULL, null=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE, related_name="comments")
