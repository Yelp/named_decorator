# -*- coding: utf-8 -*-
from types import CodeType
from types import FunctionType
from six import get_function_code
from six import get_function_defaults

from five import code_type_args_for_rename
from five import get_function_closure
from five import get_function_globals


def rename(decorator, original_func):
    """Takes an existing decorator and renames its code object to
    incorporate the wrapped function name.
    """
    c = get_function_code(decorator)

    updated_decorator_name = '{}@{}'.format(
        decorator.__name__,
        original_func.__name__,
    )

    code_type_args = code_type_args_for_rename(c, updated_decorator_name)
    code = CodeType(*code_type_args)

    return FunctionType(
        code,  # Use our updated code object
        get_function_globals(decorator),
        updated_decorator_name,
        get_function_defaults(decorator),
        get_function_closure(decorator),
    )


def named_decorator(original_func):
    """Decorator to name a wrapper after its callee. Usage:
        def my_decorator(func):
            @named_decorator(func)
            def wrapper(*args, **kwargs):
                # do things
                return method(*args, **kwargs)
    """
    def renaming_wrapper(wrapper):
        return rename(wrapper, original_func)
    return renaming_wrapper
