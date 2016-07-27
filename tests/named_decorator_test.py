# -*- coding: utf-8 -*-
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
