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
