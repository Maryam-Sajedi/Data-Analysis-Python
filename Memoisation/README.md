# Fibonacci with `functools.lru_cache`

A small demo comparing a naive recursive Fibonacci implementation against one
sped up with Python's built-in memoisation decorator, `functools.lru_cache`.

## What is memoisation?

Memoisation means remembering the result of a function call so you don't have
to recompute it when the same arguments are used again. `functools.lru_cache`
(LRU = Least Recently Used) does this automatically — it's a decorator built
into the Python standard library, so there's no extra dependency required.

## Files

- `fibonacci.py` — contains both implementations and a benchmark comparing them.

## How it works

- **`fib_slow(n)`** — a plain recursive Fibonacci function. Every call
  recomputes all of its sub-calls from scratch, so runtime grows
  exponentially with `n`.
- **`fib_fast(n)`** — the same function decorated with
  `@functools.lru_cache(maxsize=None)`. Once a result for a given `n` is
  computed, it's cached, so repeated or overlapping calls are nearly instant.

## Usage

Run the script directly:

```bash
python fibonacci.py
```

Example output:

```
fib_slow(35) = 14930352  (2.731000 s)
fib_fast(35) = 14930352  (0.000012 s)
fib_fast(200) = 453973694165307953197296969697410619233826
Cache info: CacheInfo(hits=198, misses=201, maxsize=None, currsize=201)
```

(Exact timings will vary depending on your machine.)

## Key takeaways

- `fib_slow(35)` takes a noticeable amount of time because of repeated,
  redundant recursive calls (exponential time complexity).
- `fib_fast(35)` runs almost instantly since each unique sub-problem is only
  computed once and then reused.
- `fib_fast` can comfortably handle much larger inputs (e.g. `fib_fast(200)`)
  that would be impractical for the uncached version.
- `fib_fast.cache_info()` shows cache hits, misses, and current size, which
  is useful for understanding how effective the caching is.

## Requirements

- Python 3.2+ (for `functools.lru_cache`)

## License

Feel free to use and adapt this example for learning purposes.
