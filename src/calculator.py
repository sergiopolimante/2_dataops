def add(a: float, b: float) -> float:
    return a + b


def subtract(a: float, b: float) -> float:
    return a - b


def multiply(a: float, b: float) -> float:
    return a * b


def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b



# def cube(a: float) -> float:
#     return a * a * a

# def square_root(a: float) -> float:
#     return a ** 0.5

# def cube_root(a: float) -> float:
#     return a ** (1/3)

# def logarithm(a: float) -> float:
#     return math.log(a)

# def exponential(a: float) -> float:
#     return math.exp(a)