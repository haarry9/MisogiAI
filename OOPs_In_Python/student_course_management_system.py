# ---------- Course Class ----------
class Course:
    total_enrollments = 0
    all_courses = []

    def __init__(self, course_id, name, instructor, credits, capacity):
        self.course_id = course_id
        self.name = name
        self.instructor = instructor
        self.credits = credits
        self.capacity = capacity
        self.enrolled_students = {}   # student_id -> grade list
        self.waitlist = []
        Course.all_courses.append(self)

    def __str__(self):
        return f"{self.name} ({self.course_id}) - Instructor: {self.instructor}, Credits: {self.credits}"

    def get_available_spots(self):
        return self.capacity - len(self.enrolled_students)

    def get_enrollment_count(self):
        return len(self.enrolled_students)

    def is_full(self):
        return len(self.enrolled_students) >= self.capacity

    def enroll_student(self, student):
        if self.is_full():
            self.waitlist.append(student)
            return f"{student.name} added to waitlist for {self.name}"
        self.enrolled_students[student.student_id] = []
        Course.total_enrollments += 1
        return f"{student.name} enrolled in {self.name}"

    def add_grade(self, student_id, grade):
        if student_id in self.enrolled_students:
            self.enrolled_students[student_id].append(grade)

    def get_course_statistics(self):
        all_grades = [g for grades in self.enrolled_students.values() for g in grades]
        if not all_grades:
            return {"average": 0, "highest": 0, "lowest": 0, "enrollment": len(self.enrolled_students)}
        return {
            "average": round(sum(all_grades) / len(all_grades), 2),
            "highest": max(all_grades),
            "lowest": min(all_grades),
            "enrollment": len(self.enrolled_students)
        }

    @classmethod
    def get_total_enrollments(cls):
        return cls.total_enrollments


# ---------- Student Class ----------
class Student:
    all_students = []

    def __init__(self, student_id, name, email, program):
        self.student_id = student_id
        self.name = name
        self.email = email
        self.program = program
        self.enrolled_courses = {}  # course_id -> list of grades
        Student.all_students.append(self)

    def __str__(self):
        return f"{self.name} ({self.program})"

    @classmethod
    def get_total_students(cls):
        return len(cls.all_students)

    def enroll_in_course(self, course):
        if course.course_id in self.enrolled_courses:
            return f"{self.name} already enrolled in {course.name}"
        result = course.enroll_student(self)
        if "enrolled" in result:
            self.enrolled_courses[course.course_id] = []
        return result

    def add_grade(self, course_id, grade):
        if course_id in self.enrolled_courses:
            self.enrolled_courses[course_id].append(grade)

    def calculate_gpa(self):
        grade_points = []
        for course_id, grades in self.enrolled_courses.items():
            if grades:
                avg = sum(grades) / len(grades)
                gpa_points = self.convert_to_gpa(avg)
                course_obj = next((c for c in Course.all_courses if c.course_id == course_id), None)
                credits = course_obj.credits if course_obj else 1
                grade_points.append((gpa_points, credits))
        if not grade_points:
            return 0
        total_points = sum(gp * cr for gp, cr in grade_points)
        total_credits = sum(cr for _, cr in grade_points)
        return round(total_points / total_credits, 2)

    @staticmethod
    def convert_to_gpa(grade):
        if grade >= 90: return 4.0
        elif grade >= 80: return 3.0
        elif grade >= 70: return 2.0
        elif grade >= 60: return 1.0
        else: return 0.0

    def get_transcript(self):
        return {course: grades for course, grades in self.enrolled_courses.items()}

    @classmethod
    def get_average_gpa(cls):
        gpas = [s.calculate_gpa() for s in cls.all_students if s.calculate_gpa() > 0]
        return round(sum(gpas) / len(gpas), 2) if gpas else 0

    @classmethod
    def get_top_students(cls, n=3):
        ranking = sorted([(s.name, s.calculate_gpa()) for s in cls.all_students], key=lambda x: x[1], reverse=True)
        return ranking[:n]


# ---------- ✅ TEST CASES ----------
math_course = Course("MATH101", "Calculus I", "Dr. Smith", 3, 30)
physics_course = Course("PHYS101", "Physics I", "Dr. Johnson", 4, 25)
cs_course = Course("CS101", "Programming Basics", "Prof. Brown", 3, 20)

print(f"Course: {math_course}")
print(f"Available spots in Math: {math_course.get_available_spots()}")

student1 = Student("S001", "Alice Wilson", "alice@university.edu", "Computer Science")
student2 = Student("S002", "Bob Davis", "bob@university.edu", "Mathematics")
student3 = Student("S003", "Carol Lee", "carol@university.edu", "Physics")

print(f"Student: {student1}")
print(f"Total students: {Student.get_total_students()}")

enrollment1 = student1.enroll_in_course(math_course)
enrollment2 = student1.enroll_in_course(cs_course)
enrollment3 = student2.enroll_in_course(math_course)

print(f"Alice's enrollment in Math: {enrollment1}")
print(f"Math course enrollment count: {math_course.get_enrollment_count()}")

student1.add_grade("MATH101", 85.5)
student1.add_grade("CS101", 92.0)
student1.add_grade("MATH101", 78.3)

print(f"Alice's GPA: {student1.calculate_gpa()}")
print(f"Alice's transcript: {student1.get_transcript()}")

math_course.add_grade("S001", 85.5)
math_course.add_grade("S002", 78.3)
course_stats = math_course.get_course_statistics()
print(f"Math course statistics: {course_stats}")

total_enrollments = Course.get_total_enrollments()
print(f"Total enrollments across all courses: {total_enrollments}")

average_gpa = Student.get_average_gpa()
print(f"Average GPA: {average_gpa}")

top_students = Student.get_top_students(2)
print(f"Top 2 students: {top_students}")

# Enrollment limit test
for i in range(25):  # filling near capacity
    temp = Student(f"S00{i+4}", f"Student {i}", f"student{i}@uni.edu", "General")
    result = temp.enroll_in_course(math_course)

print(f"Course full status: {math_course.is_full()}")
print(f"Waitlist size: {len(math_course.waitlist)}")
