# Standard Library imports

# Core Django imports
from django.urls import path, include

# Third-party imports
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import SimpleRouter

# App imports
from .views import user_view, myuser_view, lecture_view

router = SimpleRouter()
router.register('users', user_view.UserViewSet)
urlpatterns = [
    # path('token-auth/', myuser_view.CustomTokenObtainPairView.as_view()),
    # path('token-refresh/', TokenRefreshView.as_view()),
    # path('myusers', myuser_view.User.as_view()),
    path('lectures', lecture_view.Lecture.as_view()),
    path('lectures/<int:pk>', lecture_view.LectureDetail.as_view()),
]