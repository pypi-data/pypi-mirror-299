"""
A series of functional programming tools centered around pipelines.
"""

import inspect
from functools import lru_cache, reduce, wraps
from typing import Any, Callable, Iterable, List, Protocol, Tuple, TypeVar


class PipeProtocol(Protocol):
    def __call__(self, *args: Any, **kwargs: Any) -> Any: ...

    def get_intermediate_results(self) -> List[Any]: ...


class PipelineError(Exception):
    """Custom exception for pipeline errors."""


@lru_cache(maxsize=None)
def get_func_signature(func: Callable) -> inspect.Signature:
    """Cache and return the signature of a function."""
    return inspect.signature(func)


def should_unpack(input_value: Any, func: Callable) -> bool:
    """Determine whether the input value should be unpacked for the given function."""
    if not isinstance(input_value, tuple):
        return False

    sig = get_func_signature(func)
    params = list(sig.parameters.values())

    # If there's a *args parameter, we should always unpack
    if any(param.kind == inspect.Parameter.VAR_POSITIONAL for param in params):
        return True

    # Count the number of non-default parameters
    non_default_params = sum(
        1 for param in params if param.default == inspect.Parameter.empty
    )

    # If the number of items in the tuple matches the number of non-default parameters,
    # or if there are more items than parameters (extra will go to *args if present),
    # we should unpack
    return len(input_value) == non_default_params or len(input_value) > len(params)


def make_pipe(*funcs: Callable) -> PipeProtocol:
    """
    创建一个管道函数，将多个函数串联起来，依次执行。

    Parameters
    ----------
    - `*funcs` : Callable
        - 要串联的函数列表

    Returns
    ----------
    - `PipeProtocal`
        - 一个管道执行函数
        - 该函数可以像普通函数一样调用，并返回最终结果
        - 该函数还具有 `get_intermediate_results` 方法，可以获取所有中间结果

    Raises
    ----------
    - `PipelineError`
        - _description_

    Example:
    ----------
        >>> def double(x):
        ...     return x * 2
        >>> def add_one(x):
        ...     return x + 1
        >>> pipe = make_pipe(double, add_one)
        >>> result = pipe(3)
        >>> print(result)
        7
        >>> print(pipe.get_intermediate_results())
        [6, 7]
    """

    @wraps(funcs[0])
    def pipeline(*args: Any) -> Any:
        intermediate_results = []
        current_value = None

        for i, func in enumerate(funcs):
            try:
                if i == 0:
                    # Use all arguments for the first function
                    result = func(*args)
                else:
                    if should_unpack(current_value, func):
                        result = func(*current_value)
                    else:
                        result = func(current_value)

                intermediate_results.append(result)
                current_value = result
            except Exception as e:
                raise PipelineError(
                    f"Error in function '{func.__name__}' at step {i+1}: {str(e)}"
                ) from e

        pipeline.intermediate_results = intermediate_results
        return current_value

    def get_intermediate_results() -> List[Any]:
        return getattr(pipeline, 'intermediate_results', [])

    pipeline.get_intermediate_results = get_intermediate_results
    return pipeline


T = TypeVar('T')
R = TypeVar('R')


def for_each(func: Callable[[T], R], return_list: bool = True):
    """
    创建一个函数，将给定的函数应用于可迭代对象的每个元素。
    Parameters
    ----------
    - `func` : (item: T) -> R
        - 要应用于每个元素的函数
    - `return_list` : bool, optional
        - 是否返回列表，默认为 True

    Returns
    ----------
    - (iterable: Iterable[T]) -> List[R] | Generator[R]
        - 一个新的函数，接受一个可迭代对象并返回结果列表

    Example:
    ----------
        >>> double = lambda x: x * 2
        >>> double_each = for_each(double)
        >>> result = double_each([1, 2, 3, 4])
        >>> print(result)
        [2, 4, 6, 8]
    """

    def wrapper(iterable: Iterable[T]) -> List[R]:
        res = map(func, iterable)
        if return_list:
            return list(res)
        else:
            return res

    return wrapper


def aggregate(func: Callable[[R, T], R], initial: R) -> Callable[[Iterable[T]], R]:
    """
    创建一个函数，将给定的聚合函数应用于可迭代对象的所有元素。
    Parameters
    ----------
    - `func` : `(acc: R, item: T) -> R`
        - 聚合函数，接受两个参数：累积值和当前元素
    - `initial` : `R`
        - 初始累积值

    Returns
    ----------
    - Callable[[Iterable[T]], R]
        - 一个新的函数，接受一个可迭代对象并返回聚合结果

    Example:
    ----------
        >>> sum_squares = aggregate(lambda acc, x: acc + x**2, 0)
        >>> result = sum_squares([1, 2, 3, 4])
        >>> print(result)
        30
    """

    def wrapper(iterable: Iterable[T]) -> R:
        return reduce(func, iterable, initial)

    return wrapper
