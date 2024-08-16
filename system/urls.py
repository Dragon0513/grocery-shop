from django.urls import path

from system.views import HomeView, SignUpView

from . import views

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("login/", views.sign_in, name="login"),
    path("signup/", SignUpView.as_view(), name="signup"),
]
