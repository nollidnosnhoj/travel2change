from django.db import models


class ActivityQuerySet(models.QuerySet):
    pass


class ActivityManager(models.Manager):
    def get_queryset(self):
        return ActivityQuerySet(self.model, using=self._db)

    def approved(self):
        return self.get_queryset().approved()

    def unapproved(self):
        return self.get_queryset().unapproved()
