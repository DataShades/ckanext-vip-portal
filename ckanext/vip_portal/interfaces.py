from __future__ import annotations

import enum
from typing import Optional, Union
from flask import Response
from ckan.plugins import Interface


class Access(enum.Enum):
    allowed = enum.auto()
    forbidden = enum.auto()
    unknown = enum.auto()


class IVipPortal(Interface):
    def check_vip_access_for_endpoint(
        self,
        endpoint: Union[tuple[str, str], tuple[None, None]],
        user: Optional[str],
    ) -> Access:
        """Check if user allowed to visit the endpoint.

        Return `ckanext.vip_portal.interfaces.Access` enum member from this
        method:

        * Access.allowed: user is allowed to see the endpoint
        * Access.forbidden: user is not allowed to see the endpoint
        * Access.unknown: use default logic that depends on settings

        Use `forbidden` only when you explicitly want to disallow access to the
        ednpoint. Otherwise use `unknown`: it will check configuration of the
        extension and other plugins first and only then allow/disallow visiting
        the page.

        """
        return Access.unknown

    def check_vip_access_for_path(
        self, path: str, user: Optional[str]
    ) -> Access:
        """Check if user allowed to visit the endpoint.

        See IVipPortal.check_vip_access_for_endpoint
        """
        return Access.unknown

    def make_vip_rejection_response(
        self, user: Optional[str]
    ) -> Optional[Response]:
        """Create a response for forbiddent page.

        By default, authenticated user sees 403 page and anonymous user is
        redirected to login page.

        """
        return None

    def alter_vip_rejection_response(
        self, resp: Response, user: Optional[str]
    ) -> Response:
        """Modify rejection response before it's sent to user.

        Here you can add additional headers to the rejection response. For
        anything more complex consider using
        IVipPortal.make_vip_rejection_response.

        """
        return resp
