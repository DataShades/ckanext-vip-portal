from __future__ import annotations
from typing import Optional, Union

import ckan.plugins.toolkit as tk
from ckan.plugins import PluginImplementations

from . import config, interfaces


def is_free_endpoint(
    endpoint: Union[tuple[str, str], tuple[None, None]], user: Optional[str]
) -> bool:
    for p in PluginImplementations(interfaces.IVipPortal):
        access = p.check_vip_access_for_endpoint(endpoint, user)

        if access is interfaces.Access.allowed:
            return True

        if access is interfaces.Access.forbidden:
            return False

    return config.free_access_by_default()


def is_free_path(path: str, user: Optional[str]) -> bool:
    for p in PluginImplementations(interfaces.IVipPortal):
        access = p.check_vip_access_for_path(path, user)

        if access is interfaces.Access.allowed:
            return True

        if access is interfaces.Access.forbidden:
            return False

    return False
