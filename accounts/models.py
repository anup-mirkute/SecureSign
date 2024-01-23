from django.db import models
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session

# Create your models here.
class UserLoginSessionInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=100)
    device_id = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()

    first_login_timestamp = models.DateTimeField(auto_now_add=True)
    last_login_timestamp = models.DateTimeField(auto_now_add=True)

    is_mobile = models.BooleanField(default=False)
    is_tablet = models.BooleanField(default=False)
    is_touch_capable = models.BooleanField(default=False)
    is_pc = models.BooleanField(default=False)
    is_bot = models.BooleanField(default=False)

    user_browser_family = models.CharField(max_length=30)
    user_browser_version = models.CharField(max_length=15)
    user_browser_version_string = models.CharField(max_length=15)

    user_os_family = models.CharField(max_length=30)
    user_os_version = models.CharField(max_length=15)
    user_os_version_string = models.CharField(max_length=15)

    user_device_family = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.user.username} - {self.device_id}"