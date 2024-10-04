from arm_retry import arm_retry


@arm_retry(retries=3, delay=1)
def unstable_function():
    """
    A function that randomly fails to simulate an unstable function.
    """
    import random
    if random.choice([True, False]):
        raise ValueError("Random failure occurred")
    return "Success"

def main():
    try:
        print(unstable_function())  # Test the unstable function with retries
    except Exception as e:
        print(f"Function failed after retries: {e}")

if __name__ == "__main__":
    main()