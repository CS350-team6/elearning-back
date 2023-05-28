from rest_framework.routers import SimpleRouter
from .views import VideoViewset
router = SimpleRouter()
router.register('video', VideoViewset)
urlpatterns = router.urls