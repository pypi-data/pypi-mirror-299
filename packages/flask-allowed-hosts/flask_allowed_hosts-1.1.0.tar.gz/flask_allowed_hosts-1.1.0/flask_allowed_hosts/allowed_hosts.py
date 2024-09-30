# Flask modules
from flask import abort, Flask

# Other modules
from functools import wraps
from typing import List, Callable, Union

# Local modules
from flask_allowed_hosts.validators import validate_limit_parameters
from flask_allowed_hosts.helpers import is_valid_host, get_remote_address


class AllowedHosts:
    def __init__(self, app=None, allowed_hosts: Union[List[str], str] = None, on_denied: Callable = None):
        validate_limit_parameters(allowed_hosts, on_denied)

        # Configurations
        self.app = app
        self.on_denied = on_denied
        self.allowed_hosts = allowed_hosts

        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        if self.allowed_hosts is None:
            self.allowed_hosts = app.config.get('ALLOWED_HOSTS', ["*"])

        if self.on_denied is None:
            self.on_denied = app.config.get('ALLOWED_HOSTS_ON_DENIED', None)

    def limit(self, allowed_hosts: Union[List[str], str] = None, on_denied: Callable = None):
        validate_limit_parameters(allowed_hosts, on_denied)

        if allowed_hosts is None:
            allowed_hosts = self.allowed_hosts
        if on_denied is None:
            on_denied = self.on_denied

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                request_ip = get_remote_address()
                if is_valid_host(request_ip, allowed_hosts):
                    return func(*args, **kwargs)

                if callable(on_denied):
                    return on_denied(*args, **kwargs)
                else:
                    abort(403)

            return wrapper

        return decorator


# For backward compatibility
def limit_hosts(allowed_hosts: Union[List[str], str] = None, on_denied: Callable = None):
    validate_limit_parameters(allowed_hosts, on_denied)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            request_ip = get_remote_address()
            if is_valid_host(request_ip, allowed_hosts):
                return func(*args, **kwargs)

            if callable(on_denied):
                return on_denied(*args, **kwargs)
            else:
                abort(403)

        return wrapper

    return decorator
