from django.contrib import admin
from .models import KnowHowPost, Photo, PhotoImage, Video, Bookmark


class PhotoInline(admin.TabularInline):
    model = PhotoImage


@admin.register(KnowHowPost)
class KnowHowAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "show_tags", "count_like", "only_me")
    list_per_page = 20

    def count_like(self, obj):
        return obj.like.count()

    def show_tags(self, obj):
        try:
            tags = obj.tags.names()

            if len(tags) >= 5:
                tags = tags[:5]
                tags_to_string = ",".join(tags)
                tags_to_string += "..."
            else:
                tags_to_string = ",".join(tags)
        except Exception:
            return ""

        return tags_to_string

    count_like.short_description = "좋아요 수"
    show_tags.short_description = "태그"


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):

    inlines = (PhotoInline,)

    list_per_page = 20


@admin.register(PhotoImage)
class PhotoImageAdmin(admin.ModelAdmin):
    pass


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_per_page = 20


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    pass


# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     fieldsets = (
#         (
#             "회원 정보",
#             {"fields": ("email",)},
#         ),
#     )
#     list_display = ("email", "is_kairos_superuser")

#     def is_kairos_superuser(self, obj):
#         return obj.is_superuser

#     is_kairos_superuser.short_description = "카이로스 관리자"
#     is_kairos_superuser.boolean = True
#     list_per_page = 20


# @admin.register(Profile)
# class ProfileAdmin(admin.ModelAdmin):
#     fieldsets = (
#         (
#             "개인 정보",
#             {"fields": ("user", "name")},
#         ),
#         ("소개", {"fields": ("avatar", "bio")}),
#     )
#     list_display = ("user", "name", "avatar", "bio")
#     list_per_page = 20
