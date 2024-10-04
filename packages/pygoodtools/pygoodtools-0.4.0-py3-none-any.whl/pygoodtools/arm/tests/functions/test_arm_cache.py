import time

from arm_cache import arm_lru_cache


@arm_lru_cache(maxsize=128)
def expensive_function(x, y):
    time.sleep(0.5)  # Simulate a time-consuming computation
    return x + y

def main():
    try:
        print(expensive_function(1, 2))  # First call, should compute and cache
        print(expensive_function(1, 2))  # Second call, should return cached result
        print(expensive_function(2, 3))  # New call, should compute and cache
        print(expensive_function(3, 4))  # New call, should compute and cache
        print(expensive_function(1, 2))  # Should return cached result
        print(expensive_function(4, 5))  # New call, should compute and cache, evict oldest
        print(expensive_function(2, 3))  # Should return cached result
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()