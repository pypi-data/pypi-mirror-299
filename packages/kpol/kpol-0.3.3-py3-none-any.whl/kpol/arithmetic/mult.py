class Multiply:
    """Class for multiplication operations"""
    
    @staticmethod
    def multiply_two_numbers(a, b):
        return a * b
    
    @staticmethod
    def multiply_list_of_numbers(numbers):
        result = 1
        for num in numbers:
            result *= num
        return result
    