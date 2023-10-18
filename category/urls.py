from rest_framework import routers

from category.views import (
    CategoryViewSet,
)

router = routers.DefaultRouter()
router.register("", CategoryViewSet)


urlpatterns = router.urls

app_name = "category"
