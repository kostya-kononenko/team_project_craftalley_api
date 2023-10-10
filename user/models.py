from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext as _
from django.db import models


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    class Notification(models.TextChoices):
        EMAIL = "email", "email"
        TELEGRAM = "telegram", "telegram"

    image = models.ImageField(null=True,
                              blank=True,
                              upload_to="images/profile/")
    about_myself = models.TextField(max_length=500)
    date_of_birth = models.DateField(null=True, blank=True)
    username = None
    email = models.EmailField(_("email address"), unique=True)
    city = models.CharField(max_length=50)
    brand_name = models.CharField(max_length=50)
    user_notification = models.CharField(
        max_length=25, choices=Notification.choices, default=Notification.EMAIL
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()


class RatingStarUsers(models.Model):
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
        RatingStarUsers, on_delete=models.CASCADE,
        verbose_name="star"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="ratings")

    def __str__(self):
        return f"{self.star} - {self.user.username}"

    class Meta:
        verbose_name = "Rating"
        verbose_name_plural = "Ratings"
