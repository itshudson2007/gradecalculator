import matplotlib.pyplot as plt
import statistics
import os


def load_students(file_path='data/students.txt'):
    id_to_student = {}
    name_to_id = {}
    try:
        with open(file_path, 'r') as f:
            for line in f:

                stripped_line = line.strip()

                if len(stripped_line) >= 4:
                    student_id = stripped_line[:3]
                    name = stripped_line[3:].strip()

                    if name:
                        id_to_student[student_id] = name
                        name_to_id[name.lower()] = student_id
        return id_to_student, name_to_id
    except FileNotFoundError:
        print(f'Error: Student file not found at {file_path}.')
        return {}, {}


def load_assignments(file_path='data/assignments.txt'):
    assignment_info_by_id = {}
    assignment_name_to_id = {}
    try:
        with open(file_path, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 3:
                    points = int(parts[-1])
                    assign_id = parts[-2]
                    name = " ".join(parts[:-2])

                    assignment_info_by_id[assign_id] = {
                        'name': name,
                        'points': points
                    }
                    assignment_name_to_id[name] = assign_id

        return assignment_info_by_id, assignment_name_to_id
    except FileNotFoundError:
        print(f'Error: Assignment file not found at {file_path}.')
        return {}, {}


def load_submissions(dir_path='data/submissions'):
    submissions_data = {}

    try:
        for filename in os.listdir(dir_path):
            if filename.endswith('.txt'):

                assign_id = filename.replace('.txt', '')
                file_path = os.path.join(dir_path, filename)

                with open(file_path, 'r') as f:
                    for line in f:
                        parts = line.strip().split('|')
                        if len(parts) == 3:
                            student_id = parts[0]
                            percentage = float(parts[2])

                            if student_id not in submissions_data:
                                submissions_data[student_id] = {}

                            submissions_data[student_id][assign_id] = percentage

        return submissions_data

    except FileNotFoundError:
        print(f'Error: Submissions directory not found at {dir_path}.')
        return {}


def calculate_student_grade(student_name_to_id, assignment_info_by_id, submissions):
    name = input("What is the student's name: ")


    student_id = student_name_to_id.get(name.lower())

    if student_id is None:
        print("Student not found")
        return

    total_points_earned = 0.0
    earnings = 1000.0

    student_scores = submissions.get(student_id, {})

    if not student_scores:
        return

    for assign_id, percentage in student_scores.items():
        assign_info = assignment_info_by_id.get(assign_id)

        if assign_info:
            points_possible = assign_info['points']
            received_points = (percentage / 100.0) * points_possible
            total_points_earned += received_points

    final_grade_percent = (total_points_earned / earnings) * 100.0

    rounded_grade = round(final_grade_percent)

    print(f"{rounded_grade}%")


def assignment_statistics(assignment_name_to_id, submissions):
    name = input("What is the assignment name: ")

    assign_id = assignment_name_to_id.get(name)

    if assign_id is None:
        print("Assignment not found")
        return

    scores = []

    for student_id in submissions:
        if assign_id in submissions[student_id]:
            scores.append(submissions[student_id][assign_id])

    if not scores:
        print("No scores found for this assignment.")
        return

    minimum = round(min(scores))
    maximum = round(max(scores))
    average = round(statistics.mean(scores))

    print(f"Min: {minimum}%")
    print(f"Avg: {average}%")
    print(f"Max: {maximum}%")


def assignment_graph(assignment_name_to_id, submissions):
    name = input("What is the assignment name: ")

    assign_id = assignment_name_to_id.get(name)

    if assign_id is None:
        print("Assignment not found")
        return

    scores = []
    for student_id in submissions:
        if assign_id in submissions[student_id]:
            scores.append(submissions[student_id][assign_id])

    if not scores:
        print("No scores found for this assignment.")
        return

    bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

    plt.figure(figsize=(10, 6))

    plt.hist(scores, bins=bins, edgecolor='black', alpha=0.75)

    plt.title(f'Score Distribution for {name}', fontsize=16)
    plt.xlabel('Percentage Score', fontsize=14)
    plt.ylabel('Number of Students', fontsize=14)
    plt.xticks(bins)
    plt.grid(axis='y', alpha=0.5)

    plt.show()


def main():
    id_to_student, student_name_to_id = load_students()
    assignment_info_by_id, assignment_name_to_id = load_assignments()
    submissions = load_submissions()

    print(" 1. Student grade")
    print(" 2. Assignment statistics")
    print(" 3. Assignment graph")

    selection = input('Enter your selection: ')

    if selection == '1':
        calculate_student_grade(student_name_to_id, assignment_info_by_id, submissions)
    elif selection == '2':
        assignment_statistics(assignment_name_to_id, submissions)
    elif selection == '3':
        assignment_graph(assignment_name_to_id, submissions)
    else:
        print('Invalid selection')


if __name__ == '__main__':
    main()