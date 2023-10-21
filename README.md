[![Tests](https://github.com/DataShades/ckanext-vip-portal/actions/workflows/test.yml/badge.svg?branch=master)](https://github.com/DataShades/ckanext-vip-portal/actions/workflows/test.yml)

# ckanext-vip-portal

Generic access restrictions for anonymous user.

Configure the set or endpoints/URLs that are available for the anonymous user,
and redirect to the login page if he attempts to visit non-whitelisted page.

## Requirements

Compatibility with core CKAN versions:

| CKAN version | Compatible? |
|--------------|-------------|
| 2.9          | yes         |
| 2.10         | yes         |
| 2.11(master) | yes         |


## Installation

To install `ckanext-vip-portal`:

2. Install it using pip
   ```sh
   pip install ckanext-vip-portal
   ```

3. Add `vip_portal` to the `ckan.plugins` setting in your CKAN
   config file.


## Config settings

```ini
# Configure endpoint that handles unauthorized page access
# (optional, default: user.login)
ckanext.vip_portal.login_endpoint = auth_ext.login

# Allow anonymous access to all the pages. It basically disables current
# extensions
# (optional, default: false)
ckanext.vip_portal.free_anonymous_access = true

# Allow any authenticated user to visit pages normally
# (optional, default: true)
ckanext.vip_portal.free_authenticated_access = false

# Unless endpoint is blocked by one of IVipAccess implementations, it can be
# accessed by anyone. Use it in combination with IVipPortal interface if you
# want to leave the portal generally open and block only certain endpoints
# (optional, default: false)
ckanext.vip_portal.free_access_by_default = true

# Allow anonymous access to login pages
# (optional, default: true)
ckanext.vip_portal.allow_login = false

# Allow anonymous access to password reset page
# (optional, default: true)
ckanext.vip_portal.allow_password_reset = false

# Allow anonymous access to registration pages
# (optional, default: true)
ckanext.vip_portal.allow_registration = false

# Allow anonymous access to API endpoints
# (optional, default: true)
ckanext.vip_portal.allow_api = false

# Additional endpoints that are accessible by anonymous user
# (optional, default: )
ckanext.vip_portal.extra_allowed_endpoints = home.index home.about dataset.search

# Additional paths(URLs) that are accessible by anonymous user
# (optional, default: )
ckanext.vip_portal.extra_allowed_paths = / /about /dataset

# Allow anonymous user to access any path that starts with the following
# prefixes
# (optional, default: )
ckanext.vip_portal.extra_allowed_prefixes = /dataset /organization /group /static

# Allow anonymous user to access any path that ends with the following
# suffixes
# (optional, default: )
ckanext.vip_portal.extra_allowed_suffixes = .svg .html .css

# Allows to customize the route that the user will get redirected to
# after a successful login. Empty value allow user to be redirected to the page
# requested before displaying login page
# (optional, default: )
ckan.auth.route_after_login = dataset.search

```

## Advanced

For more specific scenarios, implement
`ckanext.vip_portal.interfaces.IVipPortal`

```python
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
```

## Developer installation

To install `ckanext-vip-portal` for development, activate your CKAN virtualenv and
do:

    git clone https://github.com/DataShades/ckanext-vip-portal.git
    cd ckanext-vip-portal
    pip install -e '.[dev]'


## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)
