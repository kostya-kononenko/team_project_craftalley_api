from rest_framework import routers

from product.views import CatalogViewSet, CategoryViewSet

router = routers.DefaultRouter()
router.register("catalog", CatalogViewSet)
router.register("category", CategoryViewSet)

urlpatterns = router.urls

app_name = "product"
