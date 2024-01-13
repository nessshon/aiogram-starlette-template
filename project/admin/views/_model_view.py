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


class CustomModelView(ModelView):

    search_builder = False
    column_visibility = True
    export_types = [ExportType.EXCEL, ExportType.PRINT]

    def can_view_details(self, request: Request) -> bool:
        """Permission for viewing full details of Item. Return True by default"""
        return AdminRoles.READ in request.state.user["roles"]

    def can_create(self, request: Request) -> bool:
        """Permission for creating new Items. Return True by default"""
        return AdminRoles.CREATE in request.state.user["roles"]

    def can_edit(self, request: Request) -> bool:
        """Permission for editing Items. Return True by default"""
        return AdminRoles.EDIT in request.state.user["roles"]

    def can_delete(self, request: Request) -> bool:
        """Permission for deleting Items. Return True by default"""
        return AdminRoles.DELETE in request.state.user["roles"]
