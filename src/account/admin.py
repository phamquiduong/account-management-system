from django.contrib import admin

from account.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email_link", "is_verified_email", "name", "is_staff", "is_active", "is_superuser")

    search_fields = ("email", "name")

    list_filter = ("is_staff", "is_active", "is_superuser", "is_verified_email")

    ordering = ("-date_joined",)

    fieldsets = (
        (None, {"fields": ("id", "email")}),
        ("Personal information", {"fields": ("name",)}),
        ("Permission", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Important", {"fields": ("last_login", "date_joined", "is_verified_email")}),
    )

    readonly_fields = ("id", "email", "last_login", "date_joined", "is_verified_email")

    list_display_links = ("email_link",)

    @admin.display(description="Email")
    def email_link(self, obj):
        return obj.email
