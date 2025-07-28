school = {
    "Math": {
        "teacher": "Mr. Smith",
        "students": [("Alice", 85), ("Bob", 92), ("Carol", 78)]
    },
    "Science": {
        "teacher": "Ms. Johnson",
        "students": [("David", 88), ("Eve", 94), ("Frank", 82)]
    }
}

# ---- 1. Print Teacher Names ----
print("Teacher Names:")
for subject, info in school.items():
    print(f"{subject} Teacher: {info['teacher']}")
print()

# ---- 2. Calculate Class Average Grades ----
print("Class Average Grades:")
for subject, info in school.items():
    students = info["students"]
    total = sum(grade for name, grade in students)  # tuple unpacking here
    avg = total / len(students)
    print(f"{subject} Average Grade: {avg:.2f}")
print()

# ---- 3. Find Top Student Across All Classes ----
top_student = None
top_grade = -1

for subject, info in school.items():
    for name, grade in info["students"]:  # tuple unpacking
        if grade > top_grade:
            top_grade = grade
            top_student = (name, grade, subject)  # store subject too for context

print("Top Student Across All Classes:")
print(f"{top_student[0]} with {top_student[1]} in {top_student[2]}")
print()

# ---- 4. Demonstrate Tuple Unpacking ----
print("Using Tuple Unpacking to Print Students:")
for subject, info in school.items():
    print(f"\n{subject} Students:")
    for name, grade in info["students"]:  # unpack tuple directly in loop
        print(f"Student: {name}, Grade: {grade}")
