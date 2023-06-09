from rest_framework.routers import SimpleRouter
from .views import VideoViewset, LectureViewset
router = SimpleRouter()
router.register('video', VideoViewset)
router.register('lectures', LectureViewset)
urlpatterns = router.urls