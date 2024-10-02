import functools
import time
import threading
import json
import asyncio
import jsonschema

# 1. Retries the function on failure
def retry(max_attempts=3, delay=1, exceptions=(Exception,)):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    print(f"Retrying {func.__name__} after {e} (attempt {attempts+1})")
                    attempts += 1
                    time.sleep(delay)
            return func(*args, **kwargs)
        return wrapper
    return decorator

# 2. Memoizes results of the function
def memoize(func):
    cache = {}
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = (args, frozenset(kwargs.items()))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    return wrapper

# 3. Throttles function execution (run once per time window)
def throttle(seconds):
    last_call = 0
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal last_call
            now = time.time()
            if now - last_call >= seconds:
                last_call = now
                return func(*args, **kwargs)
        return wrapper
    return decorator

# 4. Debounces rapid calls to a function (run only after calls have stopped)
def debounce(wait_time):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            wrapper._timer = getattr(wrapper, '_timer', None)
            if wrapper._timer:
                wrapper._timer.cancel()
            wrapper._timer = threading.Timer(wait_time, lambda: func(*args, **kwargs))
            wrapper._timer.start()
        return wrapper
    return decorator

# 5. Checks argument types
def type_check(*types):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for a, t in zip(args, types):
                if not isinstance(a, t):
                    raise TypeError(f"Expected {t} but got {type(a)}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

# 6. Checks user permissions (for example)
def require_permissions(permission):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(user, *args, **kwargs):
            if not user.has_permission(permission):
                raise PermissionError(f"User lacks permission: {permission}")
            return func(user, *args, **kwargs)
        return wrapper
    return decorator

# 7. Singleton class decorator
def singleton(cls):
    instances = {}
    @functools.wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

# 8. Logs exceptions if they occur
def log_on_exception(logger):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Exception in {func.__name__}: {e}")
                raise
        return wrapper
    return decorator

# 9. Retries on specific exceptions
def retry_on_exception(exceptions, retries=3):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(retries):
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    continue
            raise Exception(f"Function {func.__name__} failed after {retries} retries")
        return wrapper
    return decorator

# 10. Rate limits function calls
def rate_limit(max_per_second):
    min_interval = 1.0 / float(max_per_second)
    def decorator(func):
        last_time_called = [0.0]
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_time_called[0]
            wait_time = min_interval - elapsed
            if wait_time > 0:
                time.sleep(wait_time)
            last_time_called[0] = time.time()
            return func(*args, **kwargs)
        return wrapper
    return decorator

# 11. Times out after a set number of seconds
def timeout(seconds):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            def timeout_handler():
                raise TimeoutError(f"{func.__name__} timed out after {seconds} seconds")
            timer = threading.Timer(seconds, timeout_handler)
            timer.start()
            try:
                result = func(*args, **kwargs)
            finally:
                timer.cancel()
            return result
        return wrapper
    return decorator

# 12. Validates JSON schema of input
def validate_json_schema(schema):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(json_data, *args, **kwargs):
            try:
                jsonschema.validate(json_data, schema)
            except jsonschema.ValidationError as e:
                raise ValueError(f"Invalid JSON data: {e}")
            return func(json_data, *args, **kwargs)
        return wrapper
    return decorator

# 13. Implements a circuit breaker (for fault tolerance)
def circuit_breaker(failure_threshold=3, recovery_timeout=30):
    def decorator(func):
        state = {'failures': 0, 'last_failure': 0}
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if state['failures'] >= failure_threshold:
                if time.time() - state['last_failure'] < recovery_timeout:
                    raise Exception("Circuit breaker is open")
                else:
                    state['failures'] = 0
            try:
                return func(*args, **kwargs)
            except Exception:
                state['failures'] += 1
                state['last_failure'] = time.time()
                raise
        return wrapper
    return decorator

# 14. Lazy property
def lazy_property(func):
    attr_name = f"_lazy_{func.__name__}"
    @property
    @functools.wraps(func)
    def wrapper(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, func(self))
        return getattr(self, attr_name)
    return wrapper

# 15. Runs function asynchronously
def run_async(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        return await asyncio.to_thread(func, *args, **kwargs)
    return wrapper

# 16. Logs parameters and results
def log_parameters(logger):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger.info(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
            result = func(*args, **kwargs)
            logger.info(f"{func.__name__} returned {result}")
            return result
        return wrapper
    return decorator

# 17. Logs execution time of the function
def log_execution_time(logger):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            elapsed_time = time.time() - start_time
            logger.info(f"{func.__name__} executed in {elapsed_time:.4f} seconds")
            return result
        return wrapper
    return decorator

# 18. Executes a callback on success
def on_success(callback):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            callback(result)
            return result
        return wrapper
    return decorator

# 19. Executes a callback on failure
def on_failure(callback):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                callback(e)
                raise
        return wrapper
    return decorator

# 20. Runs function in a separate thread
def multithreaded(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper