from rest_framework import routers

from comment.views import CommentViewSet

router = routers.DefaultRouter()
router.register("", CommentViewSet)


urlpatterns = router.urls

app_name = "comment"
