from django.contrib import admin
from django.contrib.auth.admin import (
    UserAdmin as BaseUserAdmin,
)  # making the password field hidden
from .models import CustomUser


class CustomUserAdmin(BaseUserAdmin):
    list_display = (
        "email",
        "user_name",
        "first_name",
        "last_name",
        "is_admin",
        "is_staff",
    )
    search_fields = ("email", "user_name", "first_name")
    readonly_fields = ("date_joined", "last_login")
    ordering = ("email",)

    filter_horizontal = ()
    list_filter = ("is_admin", "is_staff", "is_active", "is_superadmin")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "user_name",
                    "first_name",
                    "last_name",
                    "phone_number",
                    "password",
                )
            },
        ),
        (
            "Permissions",
            {"fields": ("is_admin", "is_staff", "is_active", "is_superadmin")},
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "user_name",
                    "first_name",
                    "last_name",
                    "phone_number",
                    "password1",
                    "password2",
                ),
            },
        ),
    )


admin.site.register(CustomUser, CustomUserAdmin)
