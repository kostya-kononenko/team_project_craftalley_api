from rest_framework import serializers

from payment.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            "id",
            "status",
            "payment_type",
            "session_url",
            "session_id",
            "money_to_pay",
            "user",
            "cart",
        )


class PaymentListSerializer(PaymentSerializer):
    user = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Payment
        fields = (
            "id",
            "status",
            "payment_type",
            "session_url",
            "session_id",
            "money_to_pay",
            "user",
            "cart",
        )


class PaymentDetailSerializer(PaymentSerializer):
    user = serializers.CharField(source="user.email")

    class Meta:
        model = Payment
        fields = (
            "id",
            "status",
            "payment_type",
            "session_url",
            "session_id",
            "money_to_pay",
            "user",
            "cart",
        )
