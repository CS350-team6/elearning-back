from django.urls import path
from . import views
from rest_framework.routers import SimpleRouter
from .views import UserInfoViewset, UserViewSet

router = SimpleRouter()
router.register('info', UserInfoViewset)
router.register('', UserViewSet)
# router.register('home', views.home)
# router.register('signup', views.signup)
# router.register('login', views.login)
# router.register('logout', views.logout)
# router.register('pwchange', views.pwchange)
# router.register('pwreset', views.pwreset)
urlpatterns = router.urls

# app_name = "user_account"
# urlpatterns += [
#     # path('', UserList.as_view()),
#     # path('<int:pk>/', UserDetail.as_view()),
#     path("home/", views.home , name="home"),
#     path("signup/", views.signup, name="signup"),
#     path("login/", views.login, name="login"),
#     path("logout/", views.logout, name="logout"),
#     path("pwchange/", views.pwchange, name="pwchange"),
#     path("pwreset/", views.pwreset, name="pwreset"),    
#     # path("<int:question_id>/", views.detail, name="detail"),
#     #path("<int:question_id>/results/", views.results, name="results"),
#     #path("<int:question_id>/vote/", views.vote, name="vote"),
# ]