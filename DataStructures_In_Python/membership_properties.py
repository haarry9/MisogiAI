# Given data structures
fruits_list = ["apple", "banana", "orange", "apple", "grape"]
fruits_tuple = ("apple", "banana", "orange", "apple")
fruits_set = {"apple", "banana", "orange", "garpe"}
fruits_dict = {"apple": 5, "banana": 3, "orange": 8, "grape": 2}

# ---- 1. Check for Membership ----
print("Membership Check:")
print("apple in list? ", "apple" in fruits_list)
print("apple in tuple?", "apple" in fruits_tuple)
print("apple in set?  ", "apple" in fruits_set)
print("apple in dict? ", "apple" in fruits_dict)  # checks keys only
print()

# ---- 2. Find Length ----
print("Lengths:")
print("List:", len(fruits_list))
print("Tuple:", len(fruits_tuple))
print("Set:", len(fruits_set))
print("Dict:", len(fruits_dict))
print()

# ---- 3. Iterate and Print Elements ----
print("Iterating over List:")
for fruit in fruits_list:
    print(fruit)

print("\nIterating over Tuple:")
for fruit in fruits_tuple:
    print(fruit)

print("\nIterating over Set:")
for fruit in fruits_set:
    print(fruit)

print("\nIterating over Dict (keys):")
for fruit in fruits_dict:
    print(fruit)

print("\nIterating over Dict (keys & values):")
for fruit, count in fruits_dict.items():
    print(fruit, "->", count)
