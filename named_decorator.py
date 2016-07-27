# -*- coding: utf-8 -*-
from types import CodeType
from types import FunctionType
from six import get_function_code
from six import get_function_defaults

PY2 = str is bytes


def name_decorator(decorator, original_func):
    """Takes an existing decorator and renames its code object to incorporate
    the wrapped function name.
    """
    c = get_function_code(decorator)

    updated_decorator_name = '{}@{}'.format(
        original_func.__name__,
        decorator.__name__,
    )

    code_type_args = [
        c.co_argcount,
        c.co_nlocals,
        c.co_stacksize,
        c.co_flags,
        c.co_code,
        c.co_consts,
        c.co_names,
        c.co_varnames,
        c.co_filename,
        updated_decorator_name,
        c.co_firstlineno,
        c.co_lnotab,
        c.co_freevars,
        c.co_cellvars,
    ]

    if not PY2:
        code_type_args.insert(1, c.co_kwonlyargcount)

    code = CodeType(*code_type_args)

    if PY2:
        func_globals = decorator.func_globals
        func_closure = decorator.func_closure
    else:
        func_globals = decorator.__globals__
        func_closure = decorator.__closure__

    return FunctionType(
        code,  # Use our updated code object
        func_globals,
        updated_decorator_name,
        get_function_defaults(decorator),
        func_closure,
    )
