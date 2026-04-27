students = ["Madi", "Nurbulat", "Murat"]
grades = [90, 85, 92]

for index, name in enumerate(students, start=1):
    print(f"{index}: {name}")

for name, grade in zip(students, grades):
    print(f"Student: {name}, Grade: {grade}")

mixed_data = list(zip(students, grades))
print(mixed_data)