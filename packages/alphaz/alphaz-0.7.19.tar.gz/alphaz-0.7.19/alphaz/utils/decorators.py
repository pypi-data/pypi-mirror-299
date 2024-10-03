# MODULES
import inspect
from typing import Callable, Any


def no_none(f: Callable[..., Any]) -> Callable[..., Any]:
    """
    A decorator that checks for None values in the arguments of a function.

    If any of the arguments or keyword arguments of the function are None, a ValueError is raised.

    Args:
        f: The function to decorate.

    Returns:
        The decorated function.
    """

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        args_dict = {}
        try:
            args_name = inspect.getfullargspec(f).args
            args_dict = dict(zip(args_name, args))
        except:
            pass
        i = 0
        for arg_name, arg in args_dict.items():
            if arg is None:
                raise ValueError(
                    f"None value is not allowed for {arg_name=} at position {i}"
                )
            i += 1
        for kwarg_name, arg in kwargs.items():
            if arg is None:
                raise ValueError(
                    f"None value is not allowed for {kwarg_name=} at position {i}"
                )
            i += 1
        return f(*args, **kwargs)

    return wrapper


def overrides(interface_class):
    """
    Function override annotation.
    Corollary to @abc.abstractmethod where the override is not of an
    abstractmethod.
    Modified from answer https://stackoverflow.com/a/8313042/471376
    """

    def confirm_override(method):
        if method.__name__ not in dir(interface_class):
            raise NotImplementedError(
                'function "%s" is an @override but that'
                " function is not implemented in base"
                " class %s" % (method.__name__, interface_class)
            )

        def func():
            pass

        attr = getattr(interface_class, method.__name__)
        if type(attr) is not type(func):
            raise NotImplementedError(
                'function "%s" is an @override'
                " but that is implemented as type %s"
                " in base class %s, expected implemented"
                " type %s" % (method.__name__, type(attr), interface_class, type(func))
            )
        return method

    return confirm_override
