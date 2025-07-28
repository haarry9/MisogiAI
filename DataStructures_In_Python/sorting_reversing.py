employees = [
    ("Alice", 50000, "Engineering"),
    ("Bob", 60000, "Marketing"),
    ("Carol", 55000, "Engineering"),
    ("David", 45000, "Sales")
]

# ---- 1. Sort by Salary (Ascending & Descending) ----
# Using sorted() to return new lists
sorted_by_salary_asc = sorted(employees, key=lambda x: x[1])
sorted_by_salary_desc = sorted(employees, key=lambda x: x[1], reverse=True)

print("Sorted by Salary (Ascending):", sorted_by_salary_asc)
print("Sorted by Salary (Descending):", sorted_by_salary_desc)
print()

# ---- 2. Sort by Department, Then by Salary ----
sorted_by_dept_salary = sorted(employees, key=lambda x: (x[2], x[1]))
print("Sorted by Department, then Salary:", sorted_by_dept_salary)
print()

# ---- 3. Create a Reversed List ----
# Using slicing to reverse without modifying original
reversed_employees = employees[::-1]
print("Reversed Order (Original Unchanged):", reversed_employees)
print("Original List Still:", employees)
print()

# ---- 4. Sort by Name Length ----
sorted_by_name_length = sorted(employees, key=lambda x: len(x[0]))
print("Sorted by Name Length:", sorted_by_name_length)
print()

# ---- 5. Demonstrate .sort() vs sorted() ----
# .sort() modifies the list in place
employees_copy = employees[:]  # make a copy to preserve original
employees_copy.sort(key=lambda x: x[1])  # sort by salary ascending
print("Using .sort() (in-place by Salary Asc):", employees_copy)

# sorted() returns a new list
new_sorted_list = sorted(employees, key=lambda x: x[0])  # sort by name alphabetically
print("Using sorted() (new list by Name):", new_sorted_list)
