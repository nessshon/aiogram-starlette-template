# https://jowilf.github.io/starlette-admin/advanced/custom-field/#list-rendering

from starlette.datastructures import URL
from starlette_admin.contrib.sqla import Admin as BaseAdmin


class Admin(BaseAdmin):

    def custom_render_js(self, request) -> URL:
        return request.url_for("statics", path="js/custom_render.js")
