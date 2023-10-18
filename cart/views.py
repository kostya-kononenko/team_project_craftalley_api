from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from user.models import User
from .models import Cart
from .serializers import CartSerializer, PaymentCreateSerializer
from .calculate_price_all_item_in_cart import CartHelper


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all().order_by("id")
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user).filter(status_item=True)
        return queryset

    def get_serializer_class(self):
        if self.action == "pay_for_product":
            return PaymentCreateSerializer
        return CartSerializer

    @action(
        methods=["GET"],
        detail=False,
        url_path="checkout_cart/(?P<userId>[^/.]+)",
        url_name="checkout_cart",
    )
    def checkout(self, request, *args, **kwargs):
        try:
            user = User.objects.get(pk=int(kwargs.get("userId")))
        except Exception as e:
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={"Error": str(e)})

        cart_helper = CartHelper(user)
        checkout_details = cart_helper.prepare_cart_for_checkout()

        if not checkout_details:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"error": "Cart of user is empty."},
            )

        return Response(
            status=status.HTTP_200_OK, data={
                "checkout_details": checkout_details}
        )

    @action(
        methods=["PATCH"],
        detail=True,
        url_path="pay",

    )
    def pay_for_product(self, request, pk=None):
        """Endpoint to pay for the product"""
        serializer = self.get_serializer(
            instance=self.get_object(),
            data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,
                        status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
