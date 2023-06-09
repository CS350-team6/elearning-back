# Standard Library imports

# Core Django imports
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

# Third-party imports
from rest_framework.routers import SimpleRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# App imports
from elearning.views import user_view, lecture_view

router = SimpleRouter()
router.register('users', user_view.UserViewSet)
urlpatterns = router.urls
urlpatterns += [
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
    path('lectures', lecture_view.Lecture.as_view()),
    path('lectures/<int:pk>', lecture_view.LectureDetail.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
