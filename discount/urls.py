from rest_framework import routers

from discount.views import DiscountViewSet

router = routers.DefaultRouter()
router.register("", DiscountViewSet)

urlpatterns = router.urls

app_name = "discount"
