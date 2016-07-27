# -*- coding: utf-8 -*-
import cProfile
import pstats
import six

from named_decorator import rename
from named_decorator import named_decorator


# Simple decorator
def with_square(method):
    def square_wrapper(*args, **kwargs):
        """Dummy wrapper which squares the result of the method it wraps"""
        result = method(*args, **kwargs)
        return result*result
    return rename(square_wrapper, method)


# Meta decorator (with arg)
def with_arbitrary_power(power):
    def wrapper(method):
        @named_decorator(method)
        def power_wrapper(*args, **kwargs):
            result = method(*args, **kwargs)
            return result**power
        return power_wrapper
    return wrapper


@with_square
def wicked_sum(a, b):
    return a + b


@with_arbitrary_power(3)
def power_sum(a, b):
    return a + b


def test_decorators_work():
    assert 4, wicked_sum(1, 1)
    assert 27, power_sum(1, 2)


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
    assert '(square_wrapper@wicked_sum)' in output
    assert '(wicked_sum)' in output
    assert '(power_wrapper@power_sum)' in output
    assert '(power_sum)' in output
