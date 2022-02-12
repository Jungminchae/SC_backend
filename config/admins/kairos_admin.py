from django.contrib.admin import AdminSite
from users.models import User, Profile
from posts.models import Photo, PhotoImage, Video, KnowHowPost
from comments.models import KnowHowComment, VideoComment, PhotoComment
from config.admins.admin_config import AdminConfig
from posts.admin import KnowHowAdmin, PhotoAdmin, PhotoImageAdmin, VideoAdmin
from users.admin import UserAdmin, ProfileAdmin
from comments.admin import KnowHowCommentAdmin, VideoCommentAdmin, PhotoCommentAdmin


class KairosAdmin(AdminSite):
    pass


kairos_admin_site = KairosAdmin(name="KAIROS_ADMIN")

register_apps = [
    (User, UserAdmin),
    (Profile, ProfileAdmin),
    (Photo, PhotoAdmin),
    (PhotoImage, PhotoImageAdmin),
    (Video, VideoAdmin),
    (KnowHowPost, KnowHowAdmin),
    (KnowHowComment, KnowHowCommentAdmin),
    (VideoComment, VideoCommentAdmin),
    (PhotoComment, PhotoCommentAdmin),
]

kairos_admin_config = AdminConfig(
    admin_obj=kairos_admin_site, register_apps=register_apps
)
kairos_admin_config.change_admin_values("카이로스 ADMIN", "카이로스 ADMIN", "카이로스 관리")
kairos_admin_config.register_admin_apps()
