from payment.serializers import PaymentSerializer
from payment.stripe import create_stripe_session
from .models import Cart
from rest_framework import serializers


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ["id",
                  "item",
                  "quantity",
                  "created_at",
                  "updated_at",
                  "status_item"]
        read_only_fields = ("status_item", )

    def validate(self, attrs):
        item = attrs.get("item")
        cart_quantity = attrs.get("quantity")
        print(cart_quantity)

        if item.quantity == 0:
            raise serializers.ValidationError(
                f"There's no more {item.name}!"
            )
        if cart_quantity > item.quantity:
            raise serializers.ValidationError(
                f"There's no more {item.name}. Please choose less quantity!"
            )

        return attrs

    def create(self, validated_data):
        item = validated_data["item"]
        cart_quantity = validated_data["quantity"]
        cart = Cart.objects.create(
            item=item,
            quantity=item.quantity,
            status_item=True,
            user=self.context["request"].user
        )
        item.quantity -= cart_quantity
        item.save()
        return cart


class PaymentCreateSerializer(serializers.ModelSerializer):
    message = serializers.CharField(
        max_length=50,
        default="Make a payment for this product",
        read_only=True,
    )
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = (
            "message",
            "payments",
            "user",
            "item",
            "quantity",
            "created_at",
            "updated_at"
        )
        read_only_fields = (
            "message",
            "payments",
            "user",
            "item",
            "quantity",
            "created_at",
            "updated_at"
        )

    def update(self, instance, validated_data):
        create_stripe_session(instance, self.context.get("request"))
        instance.status_item = False
        instance.save()
        return instance
