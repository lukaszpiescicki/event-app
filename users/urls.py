from django.contrib.auth import views as auth_views
from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .api.views import UserModelViewSet
from .views import (
    AcceptFriendRequestView,
    ProfileUpdateView,
    SendFriendRequestView,
    UserRegisterView,
)

router = SimpleRouter()
router.register(r"users", UserModelViewSet)

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="user-register"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="users/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LoginView.as_view(template_name="users/logout.html")),
    path("accounts/profile/", ProfileUpdateView.as_view(), name="profile"),
    path(
        "send-friend-request/<int:pk>",
        SendFriendRequestView.as_view(),
        name="send_friend_request",
    ),
    path(
        "accept-friend-request/<int:pk>",
        AcceptFriendRequestView.as_view(),
        name="accept_friend_request",
    ),
    path("api/v1/", include(router.urls)),
]
