from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views
from .views import register, logout_view

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name="login.html"), name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('', views.home, name='home'),
]
