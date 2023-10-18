from django_filters import rest_framework as filters
from user.models import User


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class UserFilter(filters.FilterSet):
    brand_name = CharFilterInFilter(field_name="brand_name", lookup_expr="in")
    middle_star = filters.RangeFilter()

    class Meta:
        model = User
        fields = [
            "brand_name",
            "middle_star"
        ]
