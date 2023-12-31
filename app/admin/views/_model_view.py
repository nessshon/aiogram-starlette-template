from dataclasses import dataclass

from starlette.requests import Request
from starlette_admin import ExportType
from starlette_admin.contrib.sqla import ModelView


@dataclass
class AdminRoles:
    CREATE = "create"
    READ = "read"
    EDIT = "edit"
    DELETE = "delete"

    @classmethod
    def all(cls) -> list:
        """
         Get all admin roles as a list.

         :return: The :class:`list` of admin roles.
         """
        return [cls.CREATE, cls.READ, cls.EDIT, cls.DELETE]


class MyModelView(ModelView):
    search_builder = False
    column_visibility = True
    export_types = [ExportType.EXCEL, ExportType.PRINT]

    def can_view_details(self, request: Request) -> bool:
        return AdminRoles.READ in request.state.user["roles"]

    def can_create(self, request: Request) -> bool:
        return AdminRoles.CREATE in request.state.user["roles"]

    def can_edit(self, request: Request) -> bool:
        return AdminRoles.EDIT in request.state.user["roles"]

    def can_delete(self, request: Request) -> bool:
        return AdminRoles.DELETE in request.state.user["roles"]
