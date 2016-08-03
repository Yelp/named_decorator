# -*- coding: utf-8 -*-
import functools
from types import CodeType
from types import FunctionType
from six import get_function_code
from six import get_function_defaults
from six import PY2


def get_function_globals(func):
    """Gets a Python's function's globals. Works in Py2 and Py3.
    :param func: python function
    """
    if PY2:
        return func.func_globals
    else:
        return func.__globals__


def get_function_closure(func):
    """Gets a Python's function's closure. Works in Py2 and Py3.
    :param func: python function
    """
    if PY2:
        return func.func_closure
    else:
        return func.__closure__


def code_type_args_for_rename(code_object, updated_name):
    """Gets the list of args necessary to create a code object. This
    encapsulates differences between Py2 and Py3.

    :param code_object: Python code object
    :type code_object: code
    :param updated_name: desired name for the new code object
    :type updated_name: str

    :rtype: list
    """
    code_type_args = [
        code_object.co_argcount,
        code_object.co_nlocals,
        code_object.co_stacksize,
        code_object.co_flags,
        code_object.co_code,
        code_object.co_consts,
        code_object.co_names,
        code_object.co_varnames,
        code_object.co_filename,
        updated_name,
        code_object.co_firstlineno,
        code_object.co_lnotab,
        code_object.co_freevars,
        code_object.co_cellvars,
    ]

    if not PY2:
        code_type_args.insert(1, code_object.co_kwonlyargcount)

    return code_type_args


def named_decorator(wrapper, wrapped, decorator):
    """Takes a wrapper, a wrapped function and a decorator and renames the
    wrapper to look like wrapped@wrapper

    :param wrapper: wrapper returned by the decorator
    :type wrapper: function
    :param wrapped: wrapped function
    :type wrapped: function
    :param decorator: outer decorator
    :type decorator: function

    Usage::

        def with_log_and_call(log_message):
            def wrapper(method):
                def inner_wrapper(*args, **kwargs):
                    print(log_message)
                    return method(*args, **kargs)
                return named_decorator(inner_wrapper, method, with_log_and_call)
            return wrapper
    """
    if (
            getattr(wrapped, '__name__', None) is None or
            getattr(decorator, '__name__', None) is None
    ):
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
    This is a superset of ``functools.wraps``.

    :param wrapped: wrapped function
    :type wrapped: function
    :param decorator: outer decorator
    :type decorator: function

    Usage::

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
