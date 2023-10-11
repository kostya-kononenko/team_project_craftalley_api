from rest_framework import routers

from cart.views import CartViewSet, DeliveryCostViewSet

router = routers.DefaultRouter()
router.register(r'cart', CartViewSet)
router.register(r'delivery-cost', DeliveryCostViewSet)

urlpatterns = router.urls

app_name = "cart"
