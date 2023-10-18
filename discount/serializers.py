from rest_framework import serializers

from discount.models import Discount


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ["id",
                  "name",
                  "discount"]
