# -*- coding: utf-8 -*-
from types import CodeType
from types import FunctionType
from six import get_function_code
from six import get_function_defaults

from five import code_type_args_for_rename
from five import get_function_closure
from five import get_function_globals


def name_decorator(decorator, original_func):
    """Takes an existing decorator and renames its code object to incorporate
    the wrapped function name.
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
