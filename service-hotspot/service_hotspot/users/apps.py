import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "service_hotspot.users"
    verbose_name = _("Users")

    def ready(self):
        with contextlib.suppress(ImportError):
            import service_hotspot.users.signals  # noqa: F401
