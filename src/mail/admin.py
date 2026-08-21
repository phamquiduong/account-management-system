from django.contrib import admin

from common.admin import ReadOnlyModelAdmin
from mail.models import Email


@admin.register(Email)
class EmailAdmin(ReadOnlyModelAdmin):
    list_display = ("id", "to", "subject", "status")

    search_fields = ("to",)

    list_filter = ("status", "subject", "status")

    ordering = ("-id",)

    readonly_fields = ("id",)

    fieldsets = (
        (None, {"fields": ("id", "type")}),
        ("Receive", {"fields": ("to", "cc", "bcc")}),
        ("Content", {"fields": ("subject", "content")}),
        ("Status", {"fields": ("status", "exception")}),
    )
