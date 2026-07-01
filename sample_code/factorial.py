def factorial(n):
    """
    Compute the factorial of a non-negative integer.
    """
    if n < 0:
        raise ValueError("Factorial is undefined for negative numbers.")

    if n == 0 or n == 1:
        return 1

    result = 1
    for i in range(2, n + 1):
        result *= i

    return result


if __name__ == "__main__":
    number = 5
    print(f"{number}! = {factorial(number)}")