import functools
from types import FunctionType


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

    c = wrapper.__code__

    updated_decorator_name = f'{wrapped.__name__}@{decorator.__name__}'

    code = c.replace(co_name=updated_decorator_name)

    updated_decorator = FunctionType(
        code,  # Use our updated code object
        wrapper.__globals__,
        updated_decorator_name,
        wrapper.__defaults__,
        wrapper.__closure__,
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
