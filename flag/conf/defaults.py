from django.utils.translation import gettext_lazy as _

# reason displayed when flagging an object
FLAG_REASONS = [
        (1, _("Spam | Exists only to promote a service ")),
        (2, _("Abusive | Intended at promoting hatred")),
    ]

# number of flags before an object is marked as flagged
FLAG_ALLOWED = 10
