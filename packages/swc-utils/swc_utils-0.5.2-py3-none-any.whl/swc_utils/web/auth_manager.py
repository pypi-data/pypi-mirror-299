from copy import copy
from functools import wraps
from .request_codes import RequestCode
from flask import session, request, abort, redirect
from ..redis_database.events import get_redis_data


def get_user():
    return get_redis_data("get-user", session.get("uuid")) or {}


def check_auth() -> bool:
    return session.get("uuid") is not None


def check_admin() -> bool:
    return get_user().get("admin", False)


def get_namespaced_permissions(namespace: str) -> list:
    if not check_auth():
        return []

    permissions = get_user().get("permissions", {})
    perm_list = copy(permissions.get(namespace, []))
    perm_list.extend(permissions.get("*", []))

    return perm_list


def check_permission(namespace: str, permission: str) -> bool:
    if not check_auth():
        return False

    if check_admin():
        return True

    namespaced_permissions = get_namespaced_permissions(namespace)
    return "*" in namespaced_permissions or permission in namespaced_permissions


def auth_required(func: callable):
    @wraps(func)
    def check(*args, **kwargs):
        if check_auth():
            return func(*args, **kwargs)
        return redirect(f"/login?redirect={request.path}")

    return check


def admin_required(func: callable):
    @wraps(func)
    def check(*args, **kwargs):
        if check_admin():
            return func(*args, **kwargs)
        return abort(RequestCode.ClientError.Unauthorized)

    return check


def permission_required(namespace: str, permission: str):
    def wrapper(func):
        @wraps(func)
        def check(*args, **kwargs):
            if check_permission(namespace, permission):
                return func(*args, **kwargs)
            return abort(RequestCode.ClientError.Unauthorized)

        return check

    return wrapper
