from django.contrib import admin
from .models import KnowHowPost, Photo, PhotoImage, Video, Bookmark


@admin.register(KnowHowPost)
class KnowHowAdmin(admin.ModelAdmin):
    pass


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    pass


@admin.register(PhotoImage)
class PhotoImageAdmin(admin.ModelAdmin):
    pass


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    pass


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    pass
