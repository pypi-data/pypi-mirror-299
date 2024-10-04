from arm_type_checked import arm_is_type

@arm_is_type(int, str)
def example_function(a, b):
    return f"{a} is an integer and {b} is a string"

@arm_is_type(float, list)
def another_example_function(a, b):
    return f"{a} is a float and {b} is a list"

def main():
    try:
        print(example_function(1, "hello"))  # This should work
        print(example_function(1, 2))        # This should raise TypeError
    except Exception as e:
        print(f"Error: {e}")

    try:
        print(another_example_function(1.0, [1, 2, 3]))  # This should work
        print(another_example_function(1.0, "not a list"))  # This should raise TypeError
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()