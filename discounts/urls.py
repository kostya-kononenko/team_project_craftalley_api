from rest_framework import routers

from discounts.views import CampaignViewSet, CouponViewSet

router = routers.DefaultRouter()
router.register(r'campaign', CampaignViewSet)
router.register(r'coupon', CouponViewSet)

urlpatterns = router.urls

app_name = "discounts"
