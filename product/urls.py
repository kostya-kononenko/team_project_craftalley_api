from rest_framework import routers

from product.views import (
    ProductViewSet,
    AddProductStarRatingViewSet,
)

router = routers.DefaultRouter()
router.register("product", ProductViewSet)
router.register("rating", AddProductStarRatingViewSet)


urlpatterns = router.urls

app_name = "product"
