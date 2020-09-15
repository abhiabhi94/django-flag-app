from django.contrib import admin

from flag.models import Flag, FlagInstance


class InlineFlagInstance(admin.TabularInline):
    model = FlagInstance
    extra = 0
    readonly_fields = ['flag', 'user', 'date_flagged', 'reason', 'info']


class FlaggedContentAdmin(admin.ModelAdmin):
    list_display = ['content_object', 'creator', 'state', 'moderator', 'count']
    readonly_fields = ['content_object', 'creator', 'count']
    exclude = ['content_type', 'object_id']
    search_fields = ['content_object']
    inlines = [InlineFlagInstance]


admin.site.register(Flag, FlaggedContentAdmin)
