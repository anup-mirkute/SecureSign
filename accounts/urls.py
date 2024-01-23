from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login', views.login, name= "login"),
    path('signup', views.signup, name= "signup"),
    path('logout', views.logout, name="logout"),
    path('verify-mail/<uidb64>/<token>/', views.verifyMail, name="verify-mail"),
    path('send-verification-mail/<user>', views.sendVerificationMail, name="send-verification-mail"),
    path('password-reset/', views.sendPasswordResetMail, name="send-password-reset-mail"),
    path('reset-password/<uidb64>/<token>/', views.resetPassword, name="reset-password"),
    path('is_username_exist', views.isUsernameExist, name="is_username_exist"),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)