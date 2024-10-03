import copy
import traceback


from flask import (
    jsonify,
    make_response,
    request,
    send_file,
    send_from_directory,
    abort,
    url_for,
    render_template,
)
from enum import Enum

from ..config.main_configuration import CONFIGURATION

from ..models.main import AlphaException
from ..models.api import Parameter, ParameterMode, AlphaRequest
from ..models.api._route import Route

from core import core

api = core.api
API = core.api
DB = core.db
LOG = core.get_logger("api")

ROUTES_DISABLED = core.config.get("api/routes_disabled", [])

ROUTES = {}

# Specify the debug panels you want
# api.config['DEBUG_TB_PANELS'] = [ 'flask_debugtoolbar.panels.versions.VersionDebugPanel', 'flask_debugtoolbar.panels.timer.TimerDebugPanel', 'flask_debugtoolbar.panels.headers.HeaderDebugPanel', 'flask_debugtoolbar.panels.request_vars.RequestVarsDebugPanel', 'flask_debugtoolbar.panels.template.TemplateDebugPanel', 'flask_debugtoolbar.panels.sqlalchemy.SQLAlchemyDebugPanel', 'flask_debugtoolbar.panels.logger.LoggingPanel', 'flask_debugtoolbar.panels.profiler.ProfilerDebugPanel', 'flask_debugtoolbar_lineprofilerpanel.panels.LineProfilerPanel' ]
# toolbar = flask_debugtoolbar.DebugToolbarExtension(api)

ADMIN_USER_ID_PRIVATE = Parameter(
    "admin_user_id", ptype=int, private=True, cacheable=False
)
ADMIN_USER_ID_PUBLIC = Parameter(
    "admin_user_id", ptype=int, private=False, cacheable=False, override=True
)
ADMIN_USER_NAME_PRIVATE = Parameter(
    "admin_user_name", ptype=str, private=True, cacheable=False
)
ADMIN_USER_NAME_PUBLIC = Parameter(
    "admin_user_name", ptype=str, private=False, cacheable=False, override=True
)

default_parameters = [
    Parameter("no_log", ptype=bool, private=True, cacheable=False, default=False),
    Parameter("reset_cache", ptype=bool, default=False, private=True, cacheable=False),
    Parameter("requester", ptype=str, private=True, cacheable=False),
    Parameter("format", ptype=str, private=True, cacheable=False),
    Parameter("admin", ptype=str, private=True, cacheable=False),
    ADMIN_USER_ID_PRIVATE,
    ADMIN_USER_NAME_PRIVATE,
]


default_parameters_names = [p.name for p in default_parameters]


def get_pagination_parameters(pagination: int | None = None):
    if type(pagination) == bool:
        return [
            Parameter("page", ptype=int, default=0),
            Parameter("per_page", ptype=int),
        ]
    else:
        return [
            Parameter("page", ptype=int, default=0),
            Parameter("per_page", ptype=int, default=pagination),
        ]


def _process_parameters(
    path: str, parameters: list[Parameter], pagination: int | None = None
) -> list[Parameter]:
    parameters = [] if parameters is None else parameters
    overrides = []
    for i, parameter in enumerate(parameters):
        if type(parameter) == str:
            parameter = Parameter(parameter)
            parameters[i] = parameter
        if parameter.name in default_parameters_names:
            if parameter.override:
                overrides.append(parameter.name)
                continue
            LOG.error(
                f"Parameter could not be named <{parameter.name}> for route <{path}>!"
            )
            exit()

    output_parameter = [
        parameter for parameter in default_parameters if not parameter.name in overrides
    ]
    if pagination is not None:
        output_parameter.extend(
            [
                parameter
                for parameter in get_pagination_parameters(pagination)
                if not parameter.name in overrides
            ]
        )
    output_parameter.extend(parameters)
    return output_parameter


def route(
    path,
    parameters: list[Parameter] | None = None,
    methods=["GET"],
    cache: bool = False,
    logged: bool = False,
    admin: bool = False,
    timeout: int | None = None,
    category: str | None = None,
    description: str | None = None,
    mode: str | None = None,
    route_log: bool = True,
    access_strings: list[str] | list[Enum] = [],
    access_error_message: str | None = None,
    pagination: int | None = None,
):
    path = "/" + path if path[0] != "/" else path
    if path in ROUTES_DISABLED:
        return lambda x: x

    parameters = _process_parameters(path, parameters, pagination=pagination)

    def api_in(func):
        api.add_url_rule(path, methods=methods, view_func=func, endpoint=func.__name__)

        @api.endpoint(func.__name__)
        def api_wrapper(*args, **kwargs):
            uuid_request = AlphaRequest.get_uuid()  # ";".join(methods) + '_' +
            __route = Route(
                uuid_request,
                path,
                parameters,
                request_state=request,
                cache=cache,
                timeout=timeout,
                admin=admin,
                logged=logged,
                api=api,
                description=description,
                mode=mode,
            )
            api.routes_objects[uuid_request] = __route
            api.routes_objects = {
                x: y for x, y in api.routes_objects.items() if not y.is_outdated()
            }
            requester = __route.get("requester")
            if route_log:
                requester_head = f"{requester}: " if requester is not None else ""
                LOG.info(
                    f"{requester_head}Get api route {path} with function <{func.__name__}> and methods {','.join(methods)}"
                )

            if __route.ex is not None:
                if not __route.no_log:
                    LOG.error(ex=__route.ex)
                return __route.get_return()

            # check permissions
            if logged:
                token = (
                    AlphaRequest.get_token()
                    if api.admin_token is None
                    else api.admin_token
                )
                user = api.get_logged_user()
                status = api.get_status()

                if logged and user is None and token is None:
                    error_msg = "Wrong permission: empty token"
                    if not __route.no_log:
                        LOG.warning(error_msg)
                    __route.set_error(
                        status="wrong_access", description=error_msg, error_code=401
                    )
                    return __route.get_return()
                elif logged and user is None and status[0] == "wrong_token":
                    error_msg = "Wrong permission: wrong token"
                    if not __route.no_log:
                        LOG.warning(error_msg)
                    __route.set_error(
                        status="wrong_token", description=error_msg, error_code=401
                    )
                    return __route.get_return()
                elif logged and user is None:
                    error_msg = f"Wrong permission: {user=} not logged"
                    if not __route.no_log:
                        LOG.warning(error_msg)
                    __route.set_error(
                        status="wrong_access", description=error_msg, error_code=401
                    )
                    return __route.get_return()
                if len(access_strings) != 0:
                    new_access_strings = [
                        (
                            access_string.value
                            if isinstance(access_string, Enum)
                            else access_string
                        )
                        for access_string in access_strings
                    ]

                    is_valid_access = any(
                        [
                            x in user.permissions
                            for x in [
                                *new_access_strings,
                                *[CONFIGURATION.SUPER_USER_PERMISSION],
                            ]
                        ]
                    )
                    if not is_valid_access:
                        __route.access_denied(access_error_message)
                        return __route.get_return()
            if admin and not api.is_admin():
                __route.access_denied()
                return __route.get_return()

            """data = api.get_current_route().get_return()
            api.delete_current_route()
            return  __route.get_return()"""

            cached = __route.keep()
            if cached:
                cached = __route.get_cached()

            if not cached:
                try:
                    output = func(*args, **kwargs)
                    if output == "timeout":
                        __route.timeout()
                    elif output is not None:
                        __route.set_data(output)
                except Exception as ex:
                    error_format = api.get("error_format")
                    if error_format and error_format.lower() == "exception":
                        raise __route.set_error(ex=ex)
                    if not "alpha" in str(type(ex)).lower():
                        if not __route.no_log:
                            LOG.error(ex)
                        __route.set_error(ex=AlphaException(ex))
                    else:
                        __route.set_error(ex=ex)
                if __route.cache:
                    __route.set_cache()

            data = __route.get_return()
            # api.delete_current_route()
            return data

        api_wrapper.__name__ = func.__name__

        key_parameters = []
        for parameter in parameters:
            if parameter.name == "reset_cache" and cache:
                key_parameters.append(parameter)
            elif not parameter.private:
                key_parameters.append(parameter)

        locals_p = locals()
        if not "category" in locals_p or category is None:
            groups = func.__module__.split(".")
            current_category = groups[-1]
            if len(groups) >= 2 and groups[-2] != "routes":
                current_category = "/".join(groups[-2:])
        else:
            current_category = category.lower()

        kwargs_ = {
            "path": path,
            "parameters": key_parameters,
            "parameters_names": [x.name for x in key_parameters],
            "methods": methods,
            "cache": cache,
            "logged": logged,
            "admin": admin,
            "timeout": timeout,
            "category": current_category,
            "description": description,
        }
        api_wrapper._kwargs = kwargs_

        paths = [x for x in path.split("/") if x.strip() != ""]
        if len(paths) == 1:
            paths = ["root", paths[0]]

        arguments = {
            x: y if x != "parameters" else [j.__dict__ for j in y]
            for x, y in kwargs_.items()
        }
        for parameter in arguments["parameters"]:
            if hasattr(parameter["ptype"], "metadata"):
                if hasattr(parameter["ptype"], "type_sa_class_manager"):
                    parameter["attributes"] = parameter[
                        "ptype"
                    ].type_sa_class_manager.local_attrs

        trace = traceback.format_stack()

        ROUTES["/".join(methods) + ":" + path] = {
            "category": current_category,
            "name": func.__name__,
            "module": "",
            "paths": paths,
            "arguments": arguments,
        }

        return api_wrapper

    return api_in


##################################################################################################################
# BASE API FUNCTIONS
##################################################################################################################
CORS_CONFIG = None


@api.before_request
def before_request():
    global CORS_CONFIG
    if CORS_CONFIG is None:
        CORS_CONFIG = core.config.get("cors", {})
    if not "before" in CORS_CONFIG:
        return
    if "origins_allowed" in CORS_CONFIG["before"]:
        allowed_origins = CORS_CONFIG["before"]["origins_allowed"]
        origin = request.headers.get("Origin")
        if origin is not None and origin not in allowed_origins:
            abort(403)  # Forbidden access
    if "host_allowed" in CORS_CONFIG["before"]:
        allowed_origins = CORS_CONFIG["before"]["host_allowed"]
        origin = request.headers.get("Host")
        if origin is not None and origin not in allowed_origins:
            abort(403)  # Forbidden access


@api.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add(
        "Access-Control-Allow-Headers",
        "*",
    )
    response.headers.add("Access-Control-Allow-Methods", "*")
    # response.headers.set('Allow', 'GET, PUT, POST, DELETE, OPTIONS')
    response.headers.add("Access-Control-Allow-Credentials", "true")
    return response
