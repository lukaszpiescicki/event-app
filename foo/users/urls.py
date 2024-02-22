from django.contrib.auth import views as auth_views
from django.urls import path
from users import views as user_views

from . import views

urlpatterns = [
    path("register/", views.register, name="user-register"),
    path("login/", auth_views.LoginView.as_view(template_name="users/login.html"), name='login'),
    path("logout/", auth_views.LoginView.as_view(template_name="users/logout.html")),
    path("accounts/profile/", user_views.profile, name="profile"),
]
