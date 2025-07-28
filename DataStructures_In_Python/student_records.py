# Given data
students = [
    (101, "Alice", 85, 20),
    (102, "Bob", 92, 19),
    (103, "Carol", 78, 21),
    (104, "David", 88, 20)
]

# ---- 1. Find the Student with the Highest Grade ----
top_student = max(students, key=lambda s: s[2])  # grade is at index 2
print(f"Student with Highest Grade: {top_student[1]} ({top_student[2]})\n")

# ---- 2. Create a Name-Grade List ----
name_grade_list = [(name, grade) for _, name, grade, _ in students]
print("Name-Grade List:")
print(name_grade_list)
print()

# ---- 3. Demonstrate Tuple Immutability ----
try:
    # Attempt to change Carol's grade directly
    students[2][2] = 90
except TypeError as e:
    print("Attempt to modify tuple failed!")
    print("Error:", e)
    print("\nWhy? Tuples are immutable — you cannot change their elements once created.")
    print("This is why tuples are often used for fixed records like student data.\n")
