from cgitb import lookup
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers


class SimpleNestedURL:
    def __init__(self, parent_viewset, child_viewset, parent="", child="", lookup=""):
        self.parent_viewset = parent_viewset
        self.child_viewset = child_viewset
        self.parent = parent
        self.child = child
        self.lookup = lookup
        self.router = SimpleRouter()

    def get_nested_registered_urls(self):
        nested_routers = self._register_child_in_nested()
        nested_urls = nested_routers.urls
        return nested_urls

    def _register_child_in_nested(self):
        self._register_parent()
        child_router = routers.NestedSimpleRouter(
            self.router, self.parent, lookup=self.lookup
        )
        child_router.register(self.child, self.child_viewset)
        return child_router

    def _register_parent(self):
        self.router.register(self.parent, self.parent_viewset)
