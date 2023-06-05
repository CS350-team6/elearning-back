from rest_framework.routers import SimpleRouter
from .views.user import UserViewSet
from .views.video import VideoViewset
from .views.lecture import LectureViewset

router = SimpleRouter()
router.register('users', UserViewSet)
router.register('videos', VideoViewset, basename='video')
router.register('lectures', LectureViewset, basename='lecture')
urlpatterns = router.urls