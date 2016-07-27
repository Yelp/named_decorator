from six import PY2


def get_function_globals(func):
    if PY2:
        return func.func_globals
    else:
        return func.__globals__


def get_function_closure(func):
    if PY2:
        return func.func_closure
    else:
        return func.__closure__


def code_type_args_for_rename(c, updated_name):
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
        updated_name,
        c.co_firstlineno,
        c.co_lnotab,
        c.co_freevars,
        c.co_cellvars,
    ]

    if not PY2:
        code_type_args.insert(1, c.co_kwonlyargcount)

    return code_type_args
