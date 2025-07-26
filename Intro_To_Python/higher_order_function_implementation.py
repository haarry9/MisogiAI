# --- Custom Function Implementations ---

def custom_map(func, iterable):
    """
    Applies a function to every item of an iterable and returns a list of the results.
    """
    return [func(x) for x in iterable]

def custom_filter(func, iterable):
    """
    Constructs a list from those elements of iterable for which a function returns True.
    """
    return [x for x in iterable if func(x)]

def custom_reduce(func, iterable):
    """
    Applies a function of two arguments cumulatively to the items of an iterable,
    so as to reduce the iterable to a single value.
    """
    # Check for an empty iterable to avoid errors
    if not iterable:
        raise TypeError("custom_reduce() of empty sequence with no initial value")

    # Start with the first element as the initial result
    result = iterable[0]
    
    # Loop through the rest of the items
    for x in iterable[1:]:
        # Update the result by applying the function
        result = func(result, x)
        
    return result

# --- Sample Data ---
numbers_to_map = [1, 2, 3]
numbers_to_filter = [1, 2, 3, 4]
numbers_to_reduce = [1, 2, 3, 4]

# --- Usage with Lambda Expressions ---

print("--- Demonstrating Custom Functions ---")

# 1. Custom Map: Add 2 to each number
# The lambda x: x + 2 is the function that transforms each element.
map_result = custom_map(lambda x: x + 2, numbers_to_map)
print(f"custom_map result: {map_result}") # Expected: [3, 5, 5] (Corrected from image which shows [2, 4, 6] for x+2)
# The image shows a usage of x*2 for map, let's replicate that as well
map_result_multiply = custom_map(lambda x: x * 2, numbers_to_map)
print(f"custom_map (multiply) result: {map_result_multiply}") # Expected: [2, 4, 6]


# 2. Custom Filter: Keep only the even numbers
# The lambda x: x % 2 == 0 is the predicate function that returns True for even numbers.
filter_result = custom_filter(lambda x: x % 2 == 0, numbers_to_filter)
print(f"custom_filter result: {filter_result}") # Expected: [2, 4]


# 3. Custom Reduce: Sum all the numbers
# The lambda x, y: x + y is the cumulative function that adds the current result 'x' and the next item 'y'.
reduce_result = custom_reduce(lambda x, y: x + y, numbers_to_reduce)
print(f"custom_reduce result: {reduce_result}") # Expected: 10
