from django.apps import AppConfig
from django.db.models.signals import post_save, pre_delete


class HostsConfig(AppConfig):
    name = 'hosts'

    def ready(self):
        import hosts.signals # noqa
