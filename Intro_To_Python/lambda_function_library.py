import math
from functools import reduce

square = lambda x: x * x

add = lambda x, y: x+ y

factorial = lambda n: reduce(lambda x,y: x+y, range(1, n+1))

print("--- Math Functions ---")
print(f"Square of 9: {square(9)}")
print(f"Sum of 15 and 7: {add(15, 7)}")
print(f"Factorial of 5: {factorial(5)}")