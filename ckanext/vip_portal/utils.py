from __future__ import annotations

import ckan.plugins.toolkit as tk
from ckan.plugins import PluginImplementations

from . import config, interfaces


def is_free_endpoint(endpoint: tuple[str, str]) -> bool:
    for p in PluginImplementations(interfaces.IVipPortal):
        access = p.check_vip_access_for_endpoint(endpoint)

        if access is interfaces.Access.allowed:
            return True

        if access is interfaces.Access.forbidden:
            return False

    return False


def is_free_path(path: str) -> bool:
    for p in PluginImplementations(interfaces.IVipPortal):
        access = p.check_vip_access_for_path(path)

        if access is interfaces.Access.allowed:
            return True

        if access is interfaces.Access.forbidden:
            return False

    return False
