import matplotlib.pyplot as plt
import statistics
import os

class Student:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.submissions = {}


def load_students(file_path='data/students.txt'):
    students_by_id = {}
    name_to_id = {}

    path = os.path.join('data', 'students.txt')

    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                a = line.strip()

                if len(a) >= 4:
                    student_id = a[:3]
                    name = a[3:].strip()

                    if name:
                        obj = Student(student_id, name)
                        students_by_id[student_id] = obj
                        name_to_id[name.lower()] = student_id
        return students_by_id, name_to_id
    except FileNotFoundError:
        print(f'Error: Student file not found at {path}.')
        return {}, {}


def load_assignments(file_path='data/assignments.txt'):
    assignments_by_id = {}
    name_to_id = {}

    full_path = os.path.join('data', 'assignments.txt')

    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            while True:
                try:
                    name_line = next(f).strip()
                    if not name_line:
                        continue

                    id_line = next(f).strip()
                    points_line = next(f).strip()

                    assign_id = id_line.strip()
                    points = int(points_line)
                    name = name_line

                    assignments_by_id[assign_id] = {'name': name, 'points': points}
                    name_to_id[name] = assign_id

                except StopIteration:
                    break
                except ValueError:
                    print(f"Warning: Skipped corrupted assignment entry starting with: {name_line}")
                    continue

        return assignments_by_id, name_to_id
    except FileNotFoundError:
        print(f'Error: Assignment file not found at {full_path}.')
        return {}, {}


def load_submissions(dir_path='data/submissions', students_by_id=None):
    if students_by_id is None:
        return False

    full_dir_path = os.path.join('data', 'submissions')

    try:
        for root, dirs, files in os.walk(full_dir_path):
            for filename in files:
                if filename.endswith('.txt'):

                    file_path = os.path.join(root, filename)

                    with open(file_path, 'r', encoding='utf-8') as f:
                        for line in f:
                            parts = line.strip().split('|')
                            if len(parts) == 3:
                                student_id = parts[0].strip()
                                short_assign_id = parts[1].strip()
                                percentage = float(parts[2].strip())

                                student = students_by_id.get(student_id)

                                if student:
                                    student.submissions[short_assign_id] = percentage

        return True

    except FileNotFoundError:
        print(f'Error: Submissions directory not found at {full_dir_path}.')
        return False
    except (UnicodeDecodeError, ValueError):
        print("ERROR: File encoding or data format error in submissions file.")
        return False

def calculate(students_by_id, name_to_id, assignments_by_id):
    name = input("What is the student's name: ")

    student_id = name_to_id.get(name.lower())

    if student_id is None:
        print("Student not found")
        return

    student = students_by_id.get(student_id)

    total = 0.0
    earned = 1000.0

    if not student or not student.submissions:
        return

    for assign_id, percentage in student.submissions.items():
        assignment_info = assignments_by_id.get(assign_id)

        if assignment_info:
            points_possible = assignment_info['points']
            received_points = (percentage / 100.0) * points_possible
            total += received_points

    final_grade_percent = (total / earned) * 100.0

    rounded_grade = round(final_grade_percent)

    print(f"{rounded_grade}%")


def calculate_stats(assignments_by_id, name_to_id, students_by_id):
    name = input("What is the assignment name: ")

    assign = name_to_id.get(name)

    if assign is None:
        print("Assignment not found")
        return

    scores = []

    for student_id in students_by_id:
        student = students_by_id[student_id]
        if assign in student.submissions:
            scores.append(student.submissions[assign])

    if not scores:
        print("No scores found for this assignment.")
        return

    minimum = round(min(scores))
    maximum = round(max(scores))
    average = round(statistics.mean(scores))

    print(f"Min: {minimum}%")
    print(f"Avg: {average}%")
    print(f"Max: {maximum}%")


def graph(assignments_by_id, name_to_id, students_by_id):
    name = input("What is the assignment name: ")

    assign_id = name_to_id.get(name)

    if assign_id is None:
        print("Assignment not found")
        return

    scores = []
    for student_id in students_by_id:
        student = students_by_id[student_id]
        if assign_id in student.submissions:
            scores.append(student.submissions[assign_id])

    if not scores:
        print("No scores found for this assignment.")
        return

    bins = [50, 60, 70, 80, 90, 100]

    plt.figure(figsize=(10, 6))

    plt.hist(scores, bins=bins, edgecolor='black', alpha=0.75)

    plt.title(f'Score Distribution for {name}', fontsize=16)
    plt.xlabel('Percentage Score', fontsize=14)
    plt.ylabel('Number of Students', fontsize=14)
    plt.xticks(bins)
    plt.grid(axis='y', alpha=0.5)

    plt.show()

def main():
    students_by_id, student_name_to_id = load_students()
    assignments_by_id, assignment_name_to_id = load_assignments()

    submissions_loaded = load_submissions(students_by_id=students_by_id)

    if not students_by_id:
        print("FATAL ERROR: Could not load any student data. Check students.txt.")
    if not assignments_by_id:
        print("FATAL ERROR: Could not load any assignment data. Check assignments.txt.")
    if not submissions_loaded:
        pass

    print(" 1. Student grade")
    print(" 2. Assignment statistics")
    print(" 3. Assignment graph")

    selection = input('Enter your selection: ')

    if selection == '1':
        calculate(students_by_id, student_name_to_id, assignments_by_id)
    elif selection == '2':
        calculate_stats(assignments_by_id, assignment_name_to_id, students_by_id)
    elif selection == '3':
        graph(assignments_by_id, assignment_name_to_id, students_by_id)
    else:
        print('Invalid selection')


if __name__ == '__main__':
    main()