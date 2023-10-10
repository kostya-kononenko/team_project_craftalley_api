from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext as _

from .models import User, Rating, RatingStarUsers


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name",
                                         "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                    "user_notification",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login",
                                           "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email",
                           "password1",
                           "password2"),
            },
        ),
    )
    list_display = ("email",
                    "first_name",
                    "last_name",
                    "is_staff",
                    "user_notification")
    search_fields = ("email",
                     "first_name",
                     "last_name")
    ordering = ("email",)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("id", "star", "user")


admin.site.register(RatingStarUsers)
