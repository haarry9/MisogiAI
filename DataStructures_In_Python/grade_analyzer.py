grades = [85, 92, 78, 90, 88, 76, 94, 89, 87, 91]

print(grades[2:8])

above_85 = [g for g in grades if g > 85]
print(above_85)

grades[3] = 95

grades.extend([80, 93, 97])

top_5 = sorted(grades, reverse=True)[:5]
print(top_5)