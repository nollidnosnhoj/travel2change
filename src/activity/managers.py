from django.db import models


class ActivityManager(models.Manager):
    """
    TODO:
    - The all() function should query activites that has the is_approved = True
    - The not_approved() function should query activites that has the is_approved = False (for staff)
    """
