from __future__ import annotations

import logging
from typing import Optional

import ckan.plugins as p
import ckan.plugins.toolkit as tk

from . import config, utils, interfaces


log = logging.getLogger(__name__)


class VipPortalPlugin(p.SingletonPlugin):
    p.implements(p.IAuthenticator, inherit=True)
    p.implements(interfaces.IVipPortal, inherit=True)

    # IAuthenticator
    def identify(self):
        from ckan.views import _identify_user_default as identify

        if config.free_anonymous_access():
            return

        authenticators = p.PluginImplementations(p.IAuthenticator)
        if authenticators:
            for item in authenticators:
                if item is self:
                    continue
                if item.identify():
                    break
                try:
                    if tk.g.user:
                        break
                except AttributeError:
                    continue

        # try default identifier if no extensions have identified user up until
        # now
        if not getattr(tk.g, "user", None):
            identify()

        user = getattr(tk.g, "user", None)
        if config.free_authenticated_access() and user:
            return

        endpoint = tk.get_endpoint()
        if endpoint == (None, None):
            # page does not exist / method not allowed / etc.
            return

        if utils.is_free_endpoint(endpoint, user):
            return

        path = tk.request.path
        if utils.is_free_path(path, user):
            return

        log.debug("Unauthorized page accessed(%s): %s", endpoint, path)

        for plugin in p.PluginImplementations(interfaces.IVipPortal):
            resp = plugin.make_vip_rejection_response(user)
            if resp:
                break
        else:
            if user:
                resp = tk.abort(403, tk._("Not authorized to view this page"))
            else:
                resp = tk.h.redirect_to(config.login_endpoint())

        resp.headers.update(
            {
                "cache-control": "no-cache, no-store, must-revalidate",
                "pragma": "no-cache",
                "expires": "0",
            }
        )

        for plugin in p.PluginImplementations(interfaces.IVipPortal):
            resp = plugin.alter_vip_rejection_response(resp, user)

        return resp

    # IVipPortal
    def check_vip_access_for_endpoint(self, endpoint: tuple[str, str], user: Optional[str]) -> interfaces.Access:
        for ep in config.allowed_endpoints():
            if ep == endpoint:
                return interfaces.Access.allowed

        return super().check_vip_access_for_endpoint(endpoint, user)

    def check_vip_access_for_path(self, path: str, user: Optional[str]) -> interfaces.Access:
        allowed = config.allowed_paths()

        if path in allowed:
            return interfaces.Access.allowed

        prefixes = config.allowed_prefixes()
        for prefix in prefixes:
            if path.startswith(prefix):
                return interfaces.Access.allowed

        suffixes = config.allowed_suffixes()
        for suffix in suffixes:
            if path.endswith(suffix):
                return interfaces.Access.allowed

        return super().check_vip_access_for_path(path, user)
