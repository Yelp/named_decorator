# -*- coding: utf-8 -*-
import cProfile
import pstats
import six

from named_decorator import name_decorator


def with_square(method):
    def square_wrapper(*args, **kwargs):
        """Dummy wrapper which squares the result of the method it wraps"""
        result = method(*args, **kwargs)
        return result*result
    return name_decorator(square_wrapper, method)


@with_square
def wicked_sum(a, b):
    return a + b


def test_decorator_works():
    assert 4, wicked_sum(1, 1)


def test_wrapper_name_is_updated_under_cprofile():
    profiler = cProfile.Profile()
    profiler.enable()
    wicked_sum(1, 1)
    profiler.disable()

    s = six.StringIO()
    stats = pstats.Stats(profiler, stream=s).sort_stats()
    stats.print_stats()
    output = s.getvalue()
    assert '(square_wrapper@wicked_sum)' in output
    assert '(wicked_sum)' in output
