from django.urls import path

from system.views import (
    AccountView,
    DisclaimerView,
    HomeView,
    ImpressumView,
    PrivacyView,
    SettingsDeleteView,
    SettingsUpdateView,
    SettingsView,
    SignUpView,
    TermsView,
)

from . import views

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("account/", AccountView.as_view(), name="account"),
    path("settings/", SettingsView.as_view(), name="settings"),
    path(
        "settings/update/<int:pk>", SettingsUpdateView.as_view(), name="settings_update"
    ),
    path(
        "settings/delete/confirm/", SettingsDeleteView.as_view(), name="settings_delete"
    ),
    path("logout/", views.custom_logout, name="logout"),
    path("login/", views.sign_in, name="login"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("impressum/", ImpressumView.as_view(), name="impressum"),
    path("privacy/", PrivacyView.as_view(), name="privacy"),
    path("disclaimer/", DisclaimerView.as_view(), name="disclaimer"),
    path("terms/", TermsView.as_view(), name="terms"),
]
