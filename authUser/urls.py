from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.login, name="login"),
    path('signup', views.signup, name="signup"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)