from django.contrib import admin
from .models import KnowHowPost, KnowHowPostImage


@admin.register(KnowHowPost)
class KnowHowAdmin(admin.ModelAdmin):
    pass


@admin.register(KnowHowPostImage)
class KnowHowPostImageAdmin(admin.ModelAdmin):
    pass
