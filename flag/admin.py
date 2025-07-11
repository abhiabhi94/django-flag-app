from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from flag.models import Flag, FlagInstance


class InlineFlagInstance(admin.TabularInline):
    model = FlagInstance
    extra = 0
    readonly_fields = ["flag", "user", "date_flagged", "reason", "info"]


class FlaggedContentAdmin(admin.ModelAdmin):
    list_display = [
        "content_object",
        "creator",
        "state",
        "moderator",
        "count",
        "link_to_content_object",
    ]
    readonly_fields = ["content_object", "creator", "count", "link_to_content_object"]
    exclude = ["content_type", "object_id"]
    search_fields = ["content_object"]
    inlines = [InlineFlagInstance]

    def link_to_content_object(self, obj):
        link = reverse(
            "admin:%s_%s_change" % (obj.content_type.app_label, obj.content_type.model),
            args=[obj.object_id],
        )
        return format_html("<a href='{}'>Link</a>", link)

    link_to_content_object.short_description = _("Edit object")


admin.site.register(Flag, FlaggedContentAdmin)
