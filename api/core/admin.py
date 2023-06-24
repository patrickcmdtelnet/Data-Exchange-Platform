from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""

    ordering = ["user_id"]
    list_display = (
        "email",
        "first_name",
        "last_name",
        "phone_number",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "is_staff",
        "is_active",
        "permission_level",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                ),
            },
        ),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                )
            },
        ),
        (
            _("Security info"),
            {"fields": ("phone_number",)},
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
        (
            _("Important dates"),
            {"fields": ("last_login",)},
        ),
    )
    readonly_fields = ["last_login"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "organization",
                    "permission_level",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )
    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
        "phone_number",
    )


class PrivateSectorAdmin(admin.ModelAdmin):
    list_display = ("ps_id", "name")
    list_filter = ("created_date",)
    search_fields = ("name",)


class PublicSectorAdmin(admin.ModelAdmin):
    list_display = ("ps_id", "name")
    list_filter = ("created_date",)
    search_fields = ("name",)


class AcademiaAdmin(admin.ModelAdmin):
    list_display = ("ac_id", "name")
    list_filter = ("created_date",)
    search_fields = ("name",)


class MinistryAdmin(admin.ModelAdmin):
    list_display = ("min_id", "name")
    list_filter = ("created_date",)
    search_fields = ("name",)


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("organization_id", "name", "type", "acronym")
    list_filter = ("created_date", "type")
    search_fields = ("name", "acronym")


admin.site.register(models.User, UserAdmin)
admin.site.register(models.PrivateSector, PrivateSectorAdmin)
admin.site.register(models.PublicSector, PublicSectorAdmin)
admin.site.register(models.Academia, AcademiaAdmin)
admin.site.register(models.Ministry, MinistryAdmin)
admin.site.register(models.Organization, OrganizationAdmin)
