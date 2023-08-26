# memoization
def fib(n: int) -> int:
    memo = {}
    def dfs(n):
        # memo
        if n in memo:
            return memo[n]
        # base
        if n == 0 or n == 1:
            return n

        memo[n] = dfs(n - 1) + dfs(n - 2)
        return memo[n]
    
    return dfs(n)

# decorator syntax sugar
from functools import lru_cache
@lru_cache(maxsize=None)
def fib(n: int) -> int:
    if n == 0 or n == 1:
        return n

    return fib(n-1) + fib(n-2)
  

# custom decorator
def decorator(func): 
    cache = {}
    
    def wrapper(n):   
        if n in cache:
            return cache[n]
            
        cache[n] = func(n)
        return cache[n]

    return wrapper     

@decorator
def fib(n: int) -> int:
    if n == 0 or n == 1:
        return n

    return fib(n - 1) + fib(n - 2)
