from rest_framework import routers

from product.views import CatalogViewSet, CategoryViewSet, ProductViewSet

router = routers.DefaultRouter()
router.register("catalog", CatalogViewSet)
router.register("category", CategoryViewSet)
router.register("product", ProductViewSet)


urlpatterns = router.urls

app_name = "product"
