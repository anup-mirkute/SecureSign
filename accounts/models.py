from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings

GENDER = {
    'M' : 'Male',
    'F' : 'Female',
    'T' : 'Transgender',
}
class User(AbstractUser):
    first_name = None
    last_name = None
    name = models.CharField(max_length=50)
    is_email_verified = models.BooleanField(default=False)
    phone_no = PhoneNumberField(help_text='Contact phone number', blank=True)
    is_phone_no_verified = models.BooleanField(default=False)
    bio = models.TextField(max_length=200, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER, blank=True)
    dob = models.DateField(blank=True, null=True)
    profile_img = models.ImageField(upload_to='profile_pics/', blank=True)


class UserLoginSessionInfo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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