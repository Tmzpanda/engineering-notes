# decorator

# fibonacci
def fib(n: int) -> int:
    if n == 0:
        return 0
    elif n == 1:
        return 1

    return fib(n-1) + fib(n-2)
  
  
# fibonacci with memoization
def fib(n: int) -> int:
  
    def dfs(n: int, memo: dict) -> int:
        if n == 0:
            return 0
        elif n == 1:
            return 1

        if n not in memo:
            memo[n] = dfs(n - 1, memo) + dfs(n - 2, memo)
        
        return memo[n]

    return dfs(n, {})


# decorator syntax sugar
from functools import lru_cache
@lru_cache(maxsize=None)
def fib(n: int) -> int:
    if n == 0:
        return 0
    elif n == 1:
        return 1

    return fib(n-1) + fib(n-2)
  

# custom decorator
def decorator(func): 
    cache = {}

    def wrapper(n):   
        if n not in cache:
            cache[n] = func(n)
        return cache[n]

    return wrapper 

@decorator
def fib(n: int) -> int:
    if n == 0:
        return 0
    elif n == 1:
        return 1

    return fib(n - 1) + fib(n - 2)



