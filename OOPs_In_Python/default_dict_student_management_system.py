from collections import defaultdict

class GradeManager:
    def __init__(self):
        """
        Initialize the grade manager with appropriate defaultdict structures.
        Using defaultdict to avoid key existence checks.
        """
        # Dictionary where each student maps to another dictionary of subjects → list of grades
        self.student_grades = defaultdict(lambda: defaultdict(list))

    def add_grade(self, student_name, subject, grade):
        """
        Add a grade for a student in a specific subject.
        """
        self.student_grades[student_name][subject].append(grade)

    def get_student_average(self, student_name):
        """
        Calculate average grade for a student across all subjects.
        Returns 0 if student not found.
        """
        if student_name not in self.student_grades:
            return 0.0
        
        total = 0
        count = 0
        for grades in self.student_grades[student_name].values():
            total += sum(grades)
            count += len(grades)
        
        return round(total / count, 2) if count > 0 else 0.0

    def get_subject_statistics(self, subject):
        """
        Get statistics for a specific subject across all students.
        Returns a dictionary with average, highest, lowest, and student_count.
        """
        subject_grades = []
        for student, subjects in self.student_grades.items():
            if subject in subjects:
                subject_grades.extend(subjects[subject])
        
        if not subject_grades:
            return {"average": 0, "highest": 0, "lowest": 0, "student_count": 0}
        
        return {
            "average": round(sum(subject_grades) / len(subject_grades), 2),
            "highest": max(subject_grades),
            "lowest": min(subject_grades),
            "student_count": len([s for s in self.student_grades if subject in self.student_grades[s]])
        }

    def get_top_students(self, n=3):
        """
        Get top N students based on their overall average.
        Returns a list of tuples (student_name, average_grade) sorted by grade desc.
        """
        averages = [(student, self.get_student_average(student)) for student in self.student_grades]
        averages.sort(key=lambda x: x[1], reverse=True)
        return averages[:n]

    def get_failing_students(self, passing_grade=60):
        """
        Get students whose average is below the passing grade.
        Returns a list of tuples (student_name, average_grade).
        """
        return [(student, avg) for student, avg in 
                [(s, self.get_student_average(s)) for s in self.student_grades] 
                if avg < passing_grade]


#  Test the implementation
manager = GradeManager()

# Add sample grades
grades_data = [
    ("Alice", "Math", 85), ("Alice", "Science", 92), ("Alice", "English", 78),
    ("Bob", "Math", 75), ("Bob", "Science", 68), ("Bob", "English", 82),
    ("Charlie", "Math", 95), ("Charlie", "Science", 88), ("Charlie", "History", 91),
    ("Diana", "Math", 55), ("Diana", "Science", 62), ("Diana", "English", 70),
    ("Eve", "Math", 88), ("Eve", "Science", 94), ("Eve", "English", 86), ("Eve", "History", 89)
]

for student, subject, grade in grades_data:
    manager.add_grade(student, subject, grade)

# Test all methods
print("Alice's average:", manager.get_student_average("Alice"))
print("Math statistics:", manager.get_subject_statistics("Math"))
print("Top 3 students:", manager.get_top_students(3))
print("Failing students:", manager.get_failing_students(75))
