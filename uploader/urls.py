from rest_framework.routers import SimpleRouter
from .views import VideoViewset, LectureViewset, CommentViewset
router = SimpleRouter()
router.register('videos', VideoViewset)
router.register('lectures', LectureViewset)
router.register('comments', CommentViewset)
urlpatterns = router.urls