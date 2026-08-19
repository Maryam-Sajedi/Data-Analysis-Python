"""
@functools.lru_cache -- Free Memoisation

Memoisation means remembering the result of a function call so you do not have to recompute it when the same arguments are used again.

functools.lru_cache (LRU = Least Recently Used) does this automatically. It is a decorator built into the standard library.
"""

import functools
import time


#Fibonacci calculation:
# Without caching -- recomputes everything every call

def fib_slow(n):
    if n < 0:
        return 0
    if n <= 1:
        return 1
    return fib_slow(n - 1) + fib_slow(n - 2)


# With lru_cache -- results are stored after first computation

@functools.lru_cache(maxsize=None)
def fib_fast(n):
    if n <= 1:
        return 1
    return fib_fast(n - 1) + fib_fast(n - 2)


# Slow version -- only test up to 35 to keep it bearable
start = time.perf_counter()
result_slow = fib_slow(35)
elapsed_slow = time.perf_counter() - start
print(f"fib_slow(35) = {result_slow} ({elapsed_slow:.6f} s)")

# Fast version -- nearly instant even for large n
start = time.perf_counter()
result_fast = fib_fast(35)
elapsed_fast = time.perf_counter() - start
print(f"fib_fast(35) = {result_fast} ({elapsed_fast:.6f} s)")


# Try a much larger value -- still instant
print(f"fib_fast(200) = {fib_fast(200)}")

# See cache statistics
print(f"Cache info: {fib_fast.cache_info()}")