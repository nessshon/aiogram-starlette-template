# https://jowilf.github.io/starlette-admin/advanced/custom-field/#list-rendering

from starlette.datastructures import URL
from starlette_admin.contrib.sqla import Admin as BaseAdmin


class Admin(BaseAdmin):
    """ Class for implementing Admin interface. """

    def custom_render_js(self, request) -> URL:
        """
        Override this function to provide a link to custom js to override the
        global `render` object in javascript which is used to render fields in
        list page.

        Args:
            request: Starlette Request
        """
        return request.url_for("statics", path="js/custom_render.js")
