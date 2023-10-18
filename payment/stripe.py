import stripe

from django.urls import reverse

from cart.calculate_price_one_item import calculate_total_price_with_discount
from payment.models import Payment


stripe.api_key = "sk_test_51NmCeaF3SF8TNJQbzPAN441LtzrLV9Z0K6T9scAuXlqYIsNkQkw7OmInbExU31m7bri1BEerwlLE3vsDX8W3ZLIp00fN5Zp6UZ"


def create_payment(cart, session):
    payment = Payment.objects.create(
        status="PENDING",
        payment_type="PAYMENT",
        session_url=session.url,
        session_id=session.id,
        money_to_pay=calculate_total_price_with_discount(cart),
        user=cart.user,
        cart=cart,
    )
    return payment


def create_stripe_session(cart, request):
    success_url = (
        request.build_absolute_uri(
            reverse("payment:payment-success", args=[cart.id])
        )
        + "?session_id={CHECKOUT_SESSION_ID}"
    )
    cancel_url = (
        request.build_absolute_uri(
            reverse("payment:payment-cancel", args=[cart.id])
        )
        + "?session_id={CHECKOUT_SESSION_ID}"
    )
    total_price_in_cents = calculate_total_price_with_discount(cart)
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "unit_amount": total_price_in_cents,
                    "product_data": {
                        "name": cart.item.name,
                        "description": f"User: {cart.user.first_name} {cart.user.last_name}",
                    },
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url,
    )
    payment = create_payment(cart, session)
    cart.payments.add(payment)
    cart.save()
    return session.url
