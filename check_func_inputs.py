import sys
sys.tracebacklimit=0

def check_arg(func):
    def wrapper(*args, **kwargs):
        for i in args:
            if type(i) != int and type(i) != float:
                raise TypeError("The values must be int/float")
            
            if i < 0:
                raise ValueError("The arguments must be positive")
        
        for key, value in kwargs.items():
            if value is not int or value is not float:
                raise TypeError("The values must be int/float")
            if value < 0:
                raise ValueError("The value must be positive")
        return func(*args, **kwargs)
    return wrapper
try:
    @check_arg
    def gumar(a, b):
        return a + b
except TypeError as x:
    print(x)
except ValueError as y:
    print(y)


print(gumar(1, True))

