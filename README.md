# named_decorator

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

def my_decorator(func):
    @wraps(func, my_decorator)
    def wrapper(*args, **kwargs):
        # do things
        return method(*args, **kwargs)
    return wrapper
 ```

`@wraps` uses a function that you can import and use directly, if you prefer:

```python
from named_decorator import named_decorator

def with_log_and_call(log_message):
    def wrapper(method):
        def inner_wrapper(*args, **kwargs):
            print(log_message)
            return method(*args, **kargs)
        return named_decorator(inner_wrapper, method, with_log_and_call)
    return wrapper
```
