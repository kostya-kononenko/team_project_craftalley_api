from rest_framework import routers

from cart.views import CartViewSet

router = routers.DefaultRouter()
router.register("", CartViewSet)

urlpatterns = router.urls

app_name = "cart"
