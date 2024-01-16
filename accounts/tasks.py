from celery import shared_task
import logging

from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone

logger = logging.getLogger(__name__)

@shared_task
def delete_unverified_user():
    all_users = User.objects.filter(is_active=False)

    for user in all_users:
        # if not user.is_active:
        #     # Delete the inactive user
        #     user.delete()
        #     print(f"Deleted inactive user: {user.username}")
        # else:
        #     pass
        time_limit = user.date_joined + timedelta(days=1)
        if time_limit < timezone.now():
            user.delete()
            print(f"Deleted inactive user: {user.username}")