from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from users import views as user_views

urlpatterns = [
    path('register/', views.register, name='user-register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html')),
    path('logout/', auth_views.LoginView.as_view(template_name='users/logout.html')),
    path('profile/', user_views.profile, name='profile')
]