# -*- coding: utf-8 -*-
import cProfile
import math
import pstats
import six

from named_decorator import named_decorator
from named_decorator import wraps
from named_decorator import get_function_closure
from named_decorator import get_function_globals
from named_decorator import code_type_args_for_rename


# Simple decorator
def with_square(method):
    def wrapper(*args, **kwargs):
        """Dummy wrapper which squares the result of the method it wraps"""
        result = method(*args, **kwargs)
        return result*result
    return named_decorator(wrapper, method, with_square)


# Meta decorator (with arg)
def with_arbitrary_power(power):
    def wrapper(method):
        @wraps(method, with_arbitrary_power)
        def wrapper(*args, **kwargs):
            result = method(*args, **kwargs)
            return result**power
        return wrapper
    return wrapper


class classy_log:
    """Log function using classes, because why not"""
    def __init__(self, base):
        self.base = base

    def __call__(self, num):
        return math.log(num, self.base)


@with_square
def wicked_sum(a, b):
    "a wicked sum"
    return a + b


@with_arbitrary_power(3)
def power_sum(a, b):
    "a power sum"
    return a + b


def test_decorators_work():
    assert wicked_sum(1, 1) == 4
    assert power_sum(1, 2) == 27


def test_classy_log():
    """A bit of a special case because this function-like object does not have
    a __name__. In such a case we abort.
    """
    assert with_arbitrary_power(42)(classy_log(2))(2) == 1


def test_decorators_docs_and_name():
    """Ensures that the __doc__ and __name__ correctly carry over."""
    assert wicked_sum.__name__ == 'wicked_sum'
    assert wicked_sum.__doc__ == 'a wicked sum'

    assert power_sum.__name__ == 'power_sum'
    assert power_sum.__doc__ == 'a power sum'


def test_wrapper_name_is_updated_under_cprofile():
    """Acceptance test, to make sure the problem we're trying to solve
    (convoluted profiles) is indeed fixed.
    """
    profiler = cProfile.Profile()
    profiler.enable()
    wicked_sum(1, 2)
    power_sum(3, 4)
    profiler.disable()

    s = six.StringIO()
    stats = pstats.Stats(profiler, stream=s).sort_stats()
    stats.print_stats()
    output = s.getvalue()
    assert '(wicked_sum@with_square)' in output
    assert '(wicked_sum)' in output
    assert '(power_sum@with_arbitrary_power)' in output
    assert '(power_sum)' in output


def my_func(a, b):
    return a+b


def test_get_function_closure():
    assert get_function_closure(my_func) is None


def test_get_function_globals():
    """Smoke test to make sure this does not crash"""
    assert bool(get_function_globals(my_func)) is True


def test_code_type_args():
    expected_args_length = 14 if six.PY2 else 15
    code = six.get_function_code(my_func)
    actual_args = code_type_args_for_rename(code, 'new_name')
    assert len(actual_args) == expected_args_length
    assert 'new_name' in actual_args
