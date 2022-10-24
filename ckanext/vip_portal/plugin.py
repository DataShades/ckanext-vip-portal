from __future__ import annotations

import logging

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

        identify()
        if config.free_authenticated_access() and getattr(tk.g, "user", None):
            return

        endpoint = tk.get_endpoint()
        if utils.is_free_endpoint(endpoint):
            return

        path = tk.request.path
        if utils.is_free_path(path):
            return

        log.debug("Unauthorized page accessed(%s): %s", endpoint, path)

        for plugin in p.PluginImplementations(interfaces.IVipPortal):
            resp = plugin.make_vip_rejection_response()
            if resp:
                break
        else:
            resp = tk.h.redirect_to("user.login")

        resp.headers.update(
            {
                "cache-control": "no-cache, no-store, must-revalidate",
                "pragma": "no-cache",
                "expires": "0",
            }
        )

        for plugin in p.PluginImplementations(interfaces.IVipPortal):
            resp = plugin.alter_vip_rejection_response(resp)

        return resp
