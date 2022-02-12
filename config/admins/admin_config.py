from django.contrib import admin


class AdminConfig:
    def __init__(self, unregister_apps=None, register_apps=None, admin_obj=None):
        self.admin_obj = admin_obj
        self.unregister_apps = unregister_apps
        self.register_apps = register_apps

    def change_admin_values(self, header=None, title=None, index_title=None):
        """
        django admin setting change
        """
        if not self.admin_obj:
            admin.site.site_header = header
            admin.site.site_title = title
            admin.site.index_title = index_title
        else:
            self.admin_obj.site_header = header
            self.admin_obj.site_title = title
            self.admin_obj.index_title = index_title

    def unregister_admin_apps(self):
        for app in self.unregister_apps:
            if not app:
                break

            if not self.admin_obj:
                admin.site.unregister(app)
            else:
                self.admin_obj.unregister(app)

    def register_admin_apps(self):
        for app, _admin in self.register_apps:
            if not app:
                break
            # admin분리 했을때만 필요
            self.admin_obj.register(app, _admin)
