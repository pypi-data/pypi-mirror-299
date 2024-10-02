import time
import functools
from collections import defaultdict

# 1. Logs execution time of the function
def time_logger(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} executed in {end_time - start_time:.4f}s")
        return result
    return wrapper

# 2. Logs function calls and arguments
def simple_logger(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        return func(*args, **kwargs)
    return wrapper

# 3. Repeats function n times
def repeat(n):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(n):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

# 4. Validates argument types
def validate_types(*types):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for a, t in zip(args, types):
                if not isinstance(a, t):
                    raise TypeError(f"Expected {t} but got {type(a)}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

# 5. Caches function results
cache = {}
def cache_results(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = (args, frozenset(kwargs.items()))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    return wrapper

# 6. Measures and prints the execution time
def benchmark(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper

# 7. Converts output to uppercase
def uppercase_output(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return str(result).upper()
    return wrapper

# 8. Converts output to lowercase
def lowercase_output(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return str(result).lower()
    return wrapper

# 9. Counts how many times a function is called
call_count = defaultdict(int)
def count_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        call_count[func.__name__] += 1
        print(f"{func.__name__} has been called {call_count[func.__name__]} times")
        return func(*args, **kwargs)
    return wrapper

# 10. Debugs function arguments and return value
def debug(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Function {func.__name__} called with {args}, {kwargs}")
        result = func(*args, **kwargs)
        print(f"Function {func.__name__} returned {result}")
        return result
    return wrapper

# 11. Tracks the execution order of functions
execution_order = []
def track_execution_order(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        execution_order.append(func.__name__)
        print(f"Order of execution: {execution_order}")
        return func(*args, **kwargs)
    return wrapper

# 12. Swaps the first two arguments
def swap_arguments(func):
    @functools.wraps(func)
    def wrapper(a, b, *args, **kwargs):
        return func(b, a, *args, **kwargs)
    return wrapper

# 13. Ensures that function arguments are positive
def ensure_positive(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if any(arg < 0 for arg in args):
            raise ValueError("All arguments must be positive")
        return func(*args, **kwargs)
    return wrapper

# 14. Converts the return type to string
def convert_return_type(to_type):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return to_type(result)
        return wrapper
    return decorator

# 15. Traces function execution with timestamps
def trace(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Function {func.__name__} started at {time.strftime('%X')}")
        result = func(*args, **kwargs)
        print(f"Function {func.__name__} ended at {time.strftime('%X')}")
        return result
    return wrapper

# 16. Adds a greeting based on the time of day
def time_of_day_greeting(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        current_hour = time.localtime().tm_hour
        greeting = "Good morning" if current_hour < 12 else "Good evening"
        print(f"{greeting}, welcome to {func.__name__}!")
        return func(*args, **kwargs)
    return wrapper

# 17. Adds an exclamation mark to return value
def add_exclamation(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return f"{result}!"
    return wrapper

# 18. Silences specified exceptions
def silence_exceptions(exceptions=(Exception,)):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exceptions as e:
                print(f"Ignored exception: {e}")
        return wrapper
    return decorator

# 19. Always returns a default value
def always_return_default(default_value):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            return default_value
        return wrapper
    return decorator

# 20. Appends to a list passed in
def append_to_list(func):
    @functools.wraps(func)
    def wrapper(a_list, item):
        a_list.append(item)
        return a_list
    return wrapper