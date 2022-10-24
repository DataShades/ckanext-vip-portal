from __future__ import annotations

import enum
from typing import Optional
from flask import Response
from ckan.plugins import Interface
from . import config


class Access(enum.Enum):
    allowed = enum.auto()
    forbidden = enum.auto()
    unknown = enum.auto()


class IVipPortal(Interface):
    def check_vip_access_for_endpoint(
        self, endpoint: tuple[str, str]
    ) -> Access:
        for ep in config.allowed_endpoints():
            if ep == endpoint:
                return Access.allowed

        return Access.unknown

    def check_vip_access_for_path(self, path: str) -> Access:
        allowed = config.allowed_paths()

        if path in allowed:
            return Access.allowed

        prefixes = config.allowed_prefixes()
        for prefix in prefixes:
            if path.startswith(prefix):
                return Access.allowed

        suffixes = config.allowed_suffixes()
        for suffix in suffixes:
            if path.endswith(suffix):
                return Access.allowed

        return Access.unknown

    def make_vip_rejection_response(self) -> Optional[Response]:
        return None

    def alter_vip_rejection_response(self, resp: Response) -> Response:
        return resp
