from django.db import models


class ActivityQuerySet(models.QuerySet):
    def all(self):
        return self.filter(approved=True)

    def unapproved(self):
        return self.filter(approved=False)


class ActivityManager(models.Manager):
    def get_queryset(self):
        return ActivityQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().all()

    def unapproved(self):
        return self.get_queryset().unapproved()
