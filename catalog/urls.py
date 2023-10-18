from rest_framework import routers

from catalog.views import (
    CatalogViewSet,
)

router = routers.DefaultRouter()
router.register("", CatalogViewSet)


urlpatterns = router.urls

app_name = "catalog"
