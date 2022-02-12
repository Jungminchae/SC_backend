from django.contrib import admin
from users.models import User, Profile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "회원 정보",
            {"fields": ("email",)},
        ),
    )
    list_display = ("email", "is_kairos_superuser")

    def is_kairos_superuser(self, obj):
        return obj.is_superuser

    is_kairos_superuser.short_description = "카이로스 관리자"
    is_kairos_superuser.boolean = True
    list_per_page = 20


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "개인 정보",
            {"fields": ("user", "name")},
        ),
        ("소개", {"fields": ("avatar", "bio")}),
    )
    list_display = ("user", "name", "avatar", "bio")
    list_per_page = 20
