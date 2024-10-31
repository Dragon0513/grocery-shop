from django.urls import path

from system.views import (
    AcceptFriendRequestView,
    AccountView,
    BlockUserView,
    CancelFriendRequestView,
    CreateWarningView,
    DeclineFriendRequestView,
    DetailUserFriendsView,
    DetailUserView,
    DisclaimerView,
    HomeView,
    ImpressumView,
    NotificationsView,
    PrivacyView,
    RemoveFriendView,
    SearchView,
    SendFriendRequestView,
    SettingsDeleteView,
    SettingsUpdateView,
    SettingsView,
    SignUpView,
    TermsView,
    UnblockUserView,
    UpdateConfigUserRole,
    UpdateWarningView,
    WarningsUserView,
)

from . import views

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("notifications/", NotificationsView.as_view(), name="notifications"),
    path(
        "notifications/accept/<int:pk>/",
        AcceptFriendRequestView.as_view(),
        name="accept_friend_request",
    ),
    path(
        "notifications/decline/<int:pk>/",
        DeclineFriendRequestView.as_view(),
        name="decline_friend_request",
    ),
    path("search/", SearchView.as_view(), name="search"),
    path("profile/<int:pk>", DetailUserView.as_view(), name="profile_detail"),
    path(
        "profile/<int:pk>/friends",
        DetailUserFriendsView.as_view(),
        name="profile_friends",
    ),
    path(
        "profile/<int:pk>/send_request/",
        SendFriendRequestView.as_view(),
        name="send_friend_request",
    ),
    path(
        "profile/<int:pk>/cancel_request/",
        CancelFriendRequestView.as_view(),
        name="cancel_friend_request",
    ),
    path(
        "profile/<int:pk>/remove_friend/",
        RemoveFriendView.as_view(),
        name="remove_friend",
    ),
    path(
        "profile/<int:pk>/warnings", WarningsUserView.as_view(), name="profile_warnings"
    ),
    path(
        "profile/<int:pk>/warnings/create",
        CreateWarningView.as_view(),
        name="profile_warnings_create",
    ),
    path(
        "profile/<int:user_id>/warnings/<int:pk>/update",
        UpdateWarningView.as_view(),
        name="profile_warnings_update",
    ),
    path(
        "config/user/<int:pk>/role",
        UpdateConfigUserRole.as_view(),
        name="update_configuser_role",
    ),
    path("profile/<int:pk>/block/", BlockUserView.as_view(), name="block_user"),
    path("profile/<int:pk>/unblock/", UnblockUserView.as_view(), name="unblock_user"),
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
