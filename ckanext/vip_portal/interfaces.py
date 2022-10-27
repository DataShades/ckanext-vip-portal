from __future__ import annotations

import enum
from typing import Optional
from flask import Response
from ckan.plugins import Interface


class Access(enum.Enum):
    allowed = enum.auto()
    forbidden = enum.auto()
    unknown = enum.auto()


class IVipPortal(Interface):
    def check_vip_access_for_endpoint(
            self, endpoint: tuple[str, str], user: Optional[str]
    ) -> Access:
        return Access.unknown

    def check_vip_access_for_path(self, path: str, user: Optional[str]) -> Access:
        return Access.unknown

    def make_vip_rejection_response(self, user: Optional[str]) -> Optional[Response]:
        return None

    def alter_vip_rejection_response(self, resp: Response, user: Optional[str]) -> Response:
        return resp
