from typing import Callable, Any
from functools import wraps
import asyncio
import inspect


def cat_error(
        error_type: type = Exception,
        call: Callable[..., Any] = lambda ctx: None,
        need_raise: bool = False,
):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except error_type as e:
                ctx = {
                    'f_name': func.__name__,
                    'args': args,
                    'kwargs': kwargs,
                    'e': e,
                }
                if asyncio.iscoroutinefunction(call):
                    await call(ctx=ctx)
                else:
                    await asyncio.to_thread(call, ctx=ctx)
                if need_raise:
                    raise e

        return wrapper

    return decorator


def cat_error_bool(
        error_type: type = Exception,
):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                await func(*args, **kwargs)
                return True
            except error_type:
                return False

        return wrapper

    return decorator


def cat_error_retry(
        error_type: type = Exception,
        max_count: int = 5,
        retry_delay: float = 0.1
):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            count = -1
            while count < max_count:
                try:
                    return await func(*args, **kwargs)
                except error_type as e:
                    count += 1
                    if count == max_count:
                        raise e
                    await asyncio.sleep(retry_delay)
        return wrapper
    return decorator


def cat_error_extra(callable_name: str = 'handle_error'):
    def decorator(func):
        sig = inspect.signature(func)
        params = list(sig.parameters.values())
        params.append(
            inspect.Parameter(
                name=callable_name,
                kind=inspect.Parameter.KEYWORD_ONLY,
                default=None
            )
        )
        sig = sig.replace(parameters=params)

        @wraps(func)
        async def wrapper(*args, **kwargs):
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            handle = bound_args.arguments.pop(callable_name)
            try:
                return await func(*bound_args.args, **bound_args.kwargs)
            except Exception as e:
                if handle:
                    if inspect.iscoroutinefunction(handle):
                        return await handle(e)
                    return handle(e)

        return wrapper

    return decorator


def ckit_error(func):
    @wraps(func)
    async def async_wrapper(self, *args, **kwargs):
        try:
            return await func(self, *args, **kwargs)
        except Exception as error:
            handle_error = self.handle_error
            if inspect.iscoroutinefunction(handle_error):
                return await handle_error(func, error)
            return handle_error(func, error)

    @wraps(func)
    def sync_wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as error:
            return self.handle_error(func, error)

    if inspect.iscoroutinefunction(func):
        return async_wrapper
    return sync_wrapper
