def greet(name):
    return f"Hello, {name}!"

def add(a, b):
    return a + b

def is_even(n):
    return n % 2 == 0

def factorial(n):
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)
