from django.urls import path
from . import views

app_name = "user_account"
urlpatterns = [
    path("", views.withdraw_account , name="withdraw_account"),
    path("home/", views.home , name="home"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("pwchange/", views.pwchange, name="pwchange"),
    path("pwreset/", views.pwreset, name="pwreset"),    
    path("searchTest/", views.searchTest, name="search"),
    path("uploadTest/", views.uploadTest, name="upload"),
    path("videoTest/", views.videoTest, name="video"),
    #path("<int:question_id>/", views.detail, name="detail"),
    #path("<int:question_id>/results/", views.results, name="results"),
    #path("<int:question_id>/vote/", views.vote, name="vote"),
]