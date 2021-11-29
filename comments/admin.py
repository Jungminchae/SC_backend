from django.contrib import admin
from .models import KnowHowComment, PhotoComment, VideoComment


@admin.register(KnowHowComment)
class KnowHowCommentAdmin(admin.ModelAdmin):
    pass


@admin.register(PhotoComment)
class PhotoCommentAdmin(admin.ModelAdmin):
    pass


@admin.register(VideoComment)
class VideoCommentAdmin(admin.ModelAdmin):
    pass
