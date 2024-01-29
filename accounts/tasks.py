from celery import shared_task
import logging

# from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

logger = logging.getLogger(__name__)

@shared_task
def delete_unverified_user():
    all_users = User.objects.filter(is_active=False)

    for user in all_users:
        time_limit = user.date_joined + timedelta(days=1)
        if time_limit < timezone.now():
            user.delete()
            print(f"Deleted inactive user: {user.username}")