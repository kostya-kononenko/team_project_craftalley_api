from django_filters import rest_framework as filters

from product.models import Product


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class ProductFilter(filters.FilterSet):
    name = CharFilterInFilter(field_name="name", lookup_expr="in")
    price = filters.RangeFilter()
    category = CharFilterInFilter(field_name="category", lookup_expr="in")
    manufacturer = CharFilterInFilter(field_name="manufacturer", lookup_expr="in")
    middle_star = filters.RangeFilter()

    class Meta:
        model = Product
        fields = [
            "name",
            "price",
            "category",
            "manufacturer",
            "middle_star"
        ]
