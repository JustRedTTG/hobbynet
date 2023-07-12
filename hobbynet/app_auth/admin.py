from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

UserModel = get_user_model()

# Register your models here.

class CustomUserAdmin(UserAdmin):
    search_fields = ('email',)
    list_display = ('email', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'groups')
    filter_horizontal = ('groups', 'user_permissions',)
    ordering = ('email',)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        # ("Personal info", {"fields": ("email",)}),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("date_joined",)}),
    )

    class Meta:
        model = UserModel


admin.site.register(UserModel, CustomUserAdmin)
