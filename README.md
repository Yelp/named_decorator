# named_decorator

[![Build Status](https://travis-ci.org/Yelp/named_decorator.svg?branch=master)](https://travis-ci.org/Yelp/named_decorator)

`named_decorator` contains a utility function to dynamically rename a decorator
based on its callee (the function it wraps). This is useful especially in large
codebases with a few number of widely used decorators.

It's meant as a tool to fix situations like this one...

![convoluted profile](img/convoluted_profile.png?raw=true)

...and turn these convoluted profiles into more readable ones:

![readable profile](img/readable_profile.png?raw=true)

# Usage

```python
from named_decorator import wraps

def with_log_and_call(log_message):
    def outer_wrapper(method):
        @wraps(method, with_log_and_call)
        def wrapper(*args, **kwargs):
            print(log_message)
            return method(*args, **kargs)
    return wrapper
 ```

You can use the function form if a decorator doesn't suit you:

```python
from named_decorator import named_decorator

def with_log_and_call(log_message):
    def outer_wrapper(method):
        def wrapper(*args, **kwargs):
            print(log_message)
            return method(*args, **kargs)
        return named_decorator(wrapper, method, with_log_and_call)
    return wrapper
```

In both examples, the `wrapper` function returned by the decorator will be renamed to
`$CALLEE_NAME@with_log_and_call` to prevent call trees from getting mixed up
together by a common "`wrapper`" node.


# Why is functools.wraps insufficient?

[`functool.wraps`][functools.wraps] updates a function's `__name__`. However,
the function's code object also has a name (`.func_code.co_name`) and that is
what [cProfile][cprofile] looks at when it traces calls.

# Contributing

Use Github's pull request and issues system. To run tests:

```
tox --skip-missing-interpreters
```
`--skip-missing-interpreters` allows you to skip missing interpreters.
Those are tested by Travis CI when you issue a pull request.

[functools.wraps]: https://docs.python.org/3.5/library/functools.html#functools.wraps "functools.wraps"
[cprofile]: https://hg.python.org/cpython/file/2.7/Lib/profile.py#l289 "cprofile"
