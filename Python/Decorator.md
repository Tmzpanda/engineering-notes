### Decorator

- decorator wraps a function, modifying its behavior

- syntax sugar

  - e.g. @lru_cache

    ```python
    # decorator 
    from functools import lru_cache
    def uniquePaths(m, n):
      	
        @lru_cache # decorator - add memoization
        def rec(m, n):
            if m < 0 or n < 0: return 0
            if m == 0 and n == 0: return 1
    
            return rec(m-1, n) + rec(m, n-1)
    
        return rec(m-1, n-1)
      
      
    # recursion memoization
    def uniquePaths(m, n):
        def rec(m, n, memo):
            # if (m, n) in memo: return memo[(m, n)]
            if m < 0 or n < 0: return 0
            if m == 0 and n == 0: return 1
            
            res = rec(m-1, n, memo) + rec(m, n-1, memo)
            # memo[(m, n)] = res
            return res
    
        # memo = {}
        return rec(m-1, n-1, memo)
      
    
    # dp 
    def uniquePaths(m, n):
        dp = [[0 for _ in range(n)] for _ in range(m)]
    
        for i in range(m):
            for j in range(n):
                if i == 0 or j == 0:
                    dp[i][j] = 1
                else:
                    dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
    
        return dp[m - 1][n - 1]
    ```

  - define a decorator

    ```python
    from datetime import datetime
    
    def func_decorator(func):  # higher-order function
        def wrapper():
            if 9 <= datetime.now().hour < 23:
                func()
            else:
                pass  
    
        return wrapper # return the decorated function
    
    
    @func_decorator
    def say_whee():
        print("Whee!")
        
    
    say_whee()
    ```

    

### Decorator Design Pattern

- A structural design pattern allows behavior to be added to an individual object, dynamically, without affecting the behavior of other objects from the same class.

- e.g. [Coffee shop](https://medium.com/@minamed7atg/decorator-design-pattern-b3494339ea93)
  - SOLID - **Open/Close Principle**: classes should be open for extension, but closed for modification
  - To be continued...

