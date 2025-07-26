# 1. Filter a list to find words of a specific length

words = ["apple", "banana", "kiwi", "strawberry", "orange", "grape"]

long_words = [word for word in words if len(word) > 5]
print(long_words)

# 2. Convert a list of strings to a list of their lengths

words = ["hello", "world", "from", "python"]

words_lengths = list(map(len, words))
print(words_lengths)

# 3. Find all numbers from a list that are divisible by 3

from functions import reduce

numbers = [1, 5, 9, 12, 17, 21, 25]

product = reduce(lambda x,y: x*y, numbers)

print(product)

# 4. Find all numbers from a list that are divisible by 3

numbers = [1, 5, 9, 12, 17, 21, 25]

divisible_by_three = list(filter(lambda x: x % 3 == 0, numbers))

print(divisible_by_three)

# 5. Extract names of people older than 25 from a list of dictionaries

people = [
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 22},
    {"name": "Charlie", "age": 28},
    {"name": "Diana", "age": 24}
]

adults = [person["name"] for person in people if person["age"] > 25]

print(adults)