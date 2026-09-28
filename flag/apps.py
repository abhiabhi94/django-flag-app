from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.utils.translation import gettext_lazy as _


class FlagConfig(AppConfig):
    name = "flag"
    verbose_name = _("flag")

    def ready(self):
        import flag.signals

        post_migrate.connect(flag.signals.create_permission_groups, sender=self)
        post_migrate.connect(flag.signals.adjust_flagged_content, sender=self)
