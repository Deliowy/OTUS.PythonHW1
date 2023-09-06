#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import update_wrapper

def disable(wrapper):
    '''
    Disable a decorator by re-assigning the decorator's name
    to this function. For example, to turn off memoization:

    >>> memo = disable

    '''
    def wrapper_disable(func):
        return func
    return wrapper_disable


def decorator(func):
    '''
    Decorate a decorator so that it inherits the docstrings
    and stuff from the function it's decorating.
    '''
    def wrapper_decorator(wrapper):
        return update_wrapper(wrapper=wrapper, wrapped=func)
    return wrapper_decorator


def countcalls(func):
    '''Decorator that counts calls made to the function decorated.'''
    @decorator(func)
    def wrapper_countcalls(*args):
        wrapper_countcalls.calls +=1
        value = func(*args)
        return value
    wrapper_countcalls.calls = 0
    return wrapper_countcalls


def memo(func):
    '''
    Memoize a function so that it caches all return values for
    faster future lookups.
    '''
    @decorator(func)
    def wrapper_memo(*args):
        if args in wrapper_memo.memo:
            return wrapper_memo.memo[args]
        else:
            return wrapper_memo.memo.setdefault(args, func(*args))
    wrapper_memo.memo = {}
    return wrapper_memo
        


def n_ary(func):
    '''
    Given binary function f(x, y), return an n_ary function such
    that f(x, y, z) = f(x, f(y,z)), etc. Also allow f(x) = x.
    '''
    @decorator(func)
    def wrapper_n_ary(*args):
        if len(args) == 1:
            return args
        elif len(args)==2:
            return func(*args)
        else:
            return func(args[0], wrapper_n_ary(*args[1:]))
    return wrapper_n_ary


def trace(prefix):
    '''Trace calls made to function decorated.

    @trace("____")
    def fib(n):
        ....

    >>> fib(3)
     --> fib(3)
    ____ --> fib(2)
    ________ --> fib(1)
    ________ <-- fib(1) == 1
    ________ --> fib(0)
    ________ <-- fib(0) == 1
    ____ <-- fib(2) == 2
    ____ --> fib(1)
    ____ <-- fib(1) == 1
     <-- fib(3) == 3

    '''
    def decorator_trace(func):
        
        @decorator(func)
        def wrapper_trace(*args):
            wrapper_trace.callstack += 1
            print(f"{prefix * wrapper_trace.callstack} --> {func.__name__}({args})")
            value = func(*args)
            print(f"{prefix * wrapper_trace.callstack} <-- {func.__name__}({args}) == {value}")
            wrapper_trace.callstack -= 1
            return value
        wrapper_trace.callstack = 0
        return wrapper_trace
    return decorator_trace


@memo
@countcalls
@n_ary
def foo(a, b):
    return a + b


@countcalls
@memo
@n_ary
def bar(a, b):
    return a * b


@countcalls
@trace("####")
@memo
def fib(n):
    """Some doc"""
    return 1 if n <= 1 else fib(n-1) + fib(n-2)


def main():
    print(foo(4, 3))
    print(foo(4, 3, 2))
    print(foo(4, 3))
    print("foo was called", foo.calls, "times")

    print(bar(4, 3))
    print(bar(4, 3, 2))
    print(bar(4, 3, 2, 1))
    print("bar was called", bar.calls, "times")

    print(fib.__doc__)
    fib(3)
    print(fib.calls, 'calls made')


if __name__ == '__main__':
    main()
