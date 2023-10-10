from rest_framework import routers

from product.views import (
    CatalogViewSet,
    CategoryViewSet,
    ProductViewSet,
    AddStarRatingViewSet,
)

router = routers.DefaultRouter()
router.register("catalog", CatalogViewSet)
router.register("category", CategoryViewSet)
router.register("product", ProductViewSet)
router.register("rating", AddStarRatingViewSet)


urlpatterns = router.urls

app_name = "product"
