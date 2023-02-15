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
| 2.10         | not yet     |


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
# (optional, default: user.login).
ckanext.vip_portal.login_endpoint = auth_ext.login

# Allow anonymous access to all the pages. It basically disables
# current extensions
# (optional, default: false).
ckanext.vip_portal.free_anonymous_access = true

# Allow any authenticated user to visit pages normally
# (optional, default: true).
ckanext.vip_portal.free_authenticated_access = false

# Unless endpoint is blocked by one of IVipAccess implementations,
# it can be accessed by anyone. Use it in combination with IVipAccess
# interface if you want to leave the portal generally open and
# block only certain endpoints
# (optional, default: false).
ckanext.vip_portal.free_access_by_default = true

# Allow anonymous access to login pages
# (optional, default: true).
ckanext.vip_portal.allow_login = false

# Allow anonymous access to password reset page
# (optional, default: true).
ckanext.vip_portal.allow_password_reset = false

# Allow anonymous access to registration pages
# (optional, default: true).
ckanext.vip_portal.allow_registration = false

# Allow anonymous access to API endpoints
# (optional, default: true).
ckanext.vip_portal.allow_api = false

# Additional endpoints that are accessible by anonymous user
# (optional, default: empty).
ckanext.vip_portal.extra_allowed_endpoints = home.index home.about dataset.search

# Additional paths(URLs) that are accessible by anonymous user
# (optional, default: empty).
ckanext.vip_portal.extra_allowed_paths = / /about /dataset

# Allow anonymous user to access any path that starts with the following prefixes
# (optional, default: empty).
ckanext.vip_portal.extra_allowed_prefixes = /dataset /organization /group /static

# Allow anonymous user to access any path that ends with the following suffixes
# (optional, default: empty).
ckanext.vip_portal.extra_allowed_suffixes = .svg .html .css

```


## Developer installation

To install `ckanext-vip-portal` for development, activate your CKAN virtualenv and
do:

    git clone https://github.com/DataShades/ckanext-vip-portal.git
    cd ckanext-vip-portal
    pip install -e '.[dev]'


## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)
