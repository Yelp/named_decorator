import six
from five import get_function_closure
from five import get_function_globals
from five import code_type_args_for_rename


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
