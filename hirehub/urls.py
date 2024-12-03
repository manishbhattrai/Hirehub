from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.user_create, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/',views.users_logout, name='logout'),
    path('profile/setup/', views.profile_setup, name="profile_setup"),
]