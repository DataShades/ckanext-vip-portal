from __future__ import annotations
from collections.abc import Collection, Iterable

from typing import Any
from unittest.mock import ANY

import ckan.plugins.toolkit as tk

CONFIG_LOGIN_ENDPOINT = "ckanext.vip_portal.login_endpoint"
DEFAULT_LOGIN_ENDPOINT = "user.login"

CONFIG_FREE_ANON = "ckanext.vip_portal.free_anonymous_access"
DEFAULT_FREE_ANON = False

CONFIG_FREE_USER = "ckanext.vip_portal.free_authenticated_access"
DEFAULT_FREE_USER = True

CONFIG_ALLOW_LOGIN = "ckanext.vip_portal.allow_login"
DEFAULT_ALLOW_LOGIN = True

CONFIG_ALLOW_RESET = "ckanext.vip_portal.allow_password_reset"
DEFAULT_ALLOW_RESET = True

CONFIG_ALLOW_REGISTER = "ckanext.vip_portal.allow_registration"
DEFAULT_ALLOW_REGISTER = True

CONFIG_ALLOW_API = "ckanext.vip_portal.allow_api"
DEFAULT_ALLOW_API = True

CONFIG_EXTRA_ALLOWED_ENDPOINTS = "ckanext.vip_portal.extra_allowed_endpoints"
CONFIG_EXTRA_ALLOWED_PATHS = "ckanext.vip_portal.extra_allowed_paths"
CONFIG_EXTRA_ALLOWED_PREFIXES = "ckanext.vip_portal.extra_allowed_prefixes"
CONFIG_EXTRA_ALLOWED_SUFFIXES = "ckanext.vip_portal.extra_allowed_suffixes"

essential_endpoints = [
    ("webassets", ANY),
    ("static", ANY),
    ("_debug_toolbar", ANY),
    # ("dashboard", "index"),
]

login_endpoints = [
    ("user", "login"),
    ("user", "logged_in"),
    ("user", "logout"),
    ("user", "logged_out"),
    ("user", "logged_out_page"),
    ("user", "logged_out_redirect"),
]

password_reset_endpoints = [
    ("user", "request_reset"),
]

register_endpoints = [
    ("user", "register"),
]

api_endpoints = [
    ("api", ANY),
]


def free_anonymous_access() -> bool:
    return tk.asbool(
        tk.config.get(CONFIG_FREE_ANON, DEFAULT_FREE_ANON)
    )

def free_authenticated_access() -> bool:
    return tk.asbool(
        tk.config.get(CONFIG_FREE_USER, DEFAULT_FREE_USER)
    )

def allowed_endpoints() -> list[tuple[str, Any]]:
    endpoints: list[tuple[str, Any]] = essential_endpoints.copy()

    if tk.asbool(tk.config.get(CONFIG_ALLOW_LOGIN, DEFAULT_ALLOW_LOGIN)):
        endpoints += login_endpoints

    if tk.asbool(tk.config.get(CONFIG_ALLOW_RESET, DEFAULT_ALLOW_RESET)):
        endpoints += password_reset_endpoints

    if tk.asbool(tk.config.get(CONFIG_ALLOW_REGISTER, DEFAULT_ALLOW_REGISTER)):
        endpoints += register_endpoints

    if tk.asbool(tk.config.get(CONFIG_ALLOW_API, DEFAULT_ALLOW_API)):
        endpoints += api_endpoints

    for ep in tk.aslist(tk.config.get(CONFIG_EXTRA_ALLOWED_ENDPOINTS)):
        endpoints.append(tuple(ep.split(".")))

    return endpoints


def allowed_paths() -> Collection[str]:
    paths = {}

    paths.update(tk.aslist(tk.config.get(CONFIG_EXTRA_ALLOWED_PATHS)))

    return paths


def allowed_prefixes() -> Iterable[str]:
    prefixes = []
    prefixes += tk.aslist(tk.config.get(CONFIG_EXTRA_ALLOWED_PREFIXES))
    return prefixes


def allowed_suffixes() -> Iterable[str]:
    suffixes = []
    suffixes += tk.aslist(tk.config.get(CONFIG_EXTRA_ALLOWED_SUFFIXES))
    return suffixes


def login_endpoint() -> str:
    return tk.config.get(CONFIG_LOGIN_ENDPOINT, DEFAULT_LOGIN_ENDPOINT)
