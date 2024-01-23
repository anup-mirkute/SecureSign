from django.urls import path, include
from . import views

urlpatterns = [
    path('home', views.home, name="home"),
    path('account', views.account, name="account"),
    path('logout_device/<str:device_id>/', views.logout_device, name="logout_device"),
]