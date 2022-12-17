import functools

def arg_checker(*arg_types):
    '''An argument checker decorator that checks both:
        - The number of variables that you use for a function
        - The type of each variable.
       Raises a TypeError if either of these fail''' 
    def dec(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if len(args) != len(arg_types):
                raise TypeError(
                    f"{func.__name__} expects {len(arg_types)} arguments, got {len(args)}.")
            for i, arg in enumerate(args):
                if not isinstance(arg, arg_types[i]):
                    raise TypeError(
                        f"Argument {i} is of type {type(arg)}, expected {type(arg_types[i])}")
            return func(*args, **kwargs)
        return wrapper
    return dec
