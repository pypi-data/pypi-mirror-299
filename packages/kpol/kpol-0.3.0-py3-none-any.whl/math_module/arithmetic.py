class Arithmetic:
    """
    A simple class to perform basic arithmetic operations.
    """

    def add(self, a, b):
        """Return the sum of two numbers."""
        return a + b

    def multiply(self, a, b):
        """Return the product of two numbers."""
        return a * b

    def subtract(self, a, b):
        """Return the difference of two numbers."""
        return a - b

    def divide(self, a, b):
        """Return the division of two numbers."""
        if b != 0:
            return a / b
        else:
            raise ValueError("Cannot divide by zero.")
