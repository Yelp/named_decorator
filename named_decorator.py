# -*- coding: utf-8 -*-
import functools
from types import CodeType
from types import FunctionType
from six import get_function_code
from six import get_function_defaults

from five import code_type_args_for_rename
from five import get_function_closure
from five import get_function_globals


def named_decorator(wrapper, wrapped, decorator):
    """Takes a wrapper, a wrapped function and a decorator and rename the
    wrapper to look like wrapped@wrapper

    Sample Usage:
        def with_log_and_call(log_message):
            def wrapper(method):
                def inner_wrapper(*args, **kwargs):
                    print(log_message)
                    return method(*args, **kargs)
                return named_decorator(inner_wrapper, method, with_log_and_call)
            return wrapper
    """
    if getattr(wrapped, '__name__', None) is None:
        # If the wrapped function does not have a name, abort since we can't
        # assign a better name. This can happen if you're trying to wrap
        # function-like objects.
        return wrapper

    c = get_function_code(wrapper)

    updated_decorator_name = '{}@{}'.format(
        wrapped.__name__,
        decorator.__name__,
    )

    code_type_args = code_type_args_for_rename(c, updated_decorator_name)
    code = CodeType(*code_type_args)

    updated_decorator = FunctionType(
        code,  # Use our updated code object
        get_function_globals(wrapper),
        updated_decorator_name,
        get_function_defaults(wrapper),
        get_function_closure(wrapper),
    )
    return functools.update_wrapper(updated_decorator, wrapped)


def wraps(wrapped, decorator):
    """Decorator to name a wrapper after its callee.
    This is a superset of functools.wraps.

    Usage:
        def my_decorator(func):
            @wraps(func, my_decorator)
            def wrapper(*args, **kwargs):
                # do things
                return method(*args, **kwargs)
            return wrapper
    """
    def renaming_wrapper(wrapper):
        return named_decorator(wrapper, wrapped, decorator)
    return renaming_wrapper
