import matplotlib.pyplot as plt
import statistics
import os


def load_students(file_path='data/students.txt'):
    id_to_student = {}
    name_to_id = {}

    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip().split(', ')
                if len(line) == 2:
                    id = line[0]
                    name = line[1]
                    id_to_student[id] = name
                    name_to_id[name] = id
        return id_to_student, name_to_id
    except FileNotFoundError:
        print(f'Error: Student file not found at {file_path}')
        return {}, {}


def load_assignments(file_path='data/assignments.txt'):
    info = {}
    name_to_id = {}
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip().split(', ')
                if len(line) == 3:
                    id = line[0]
                    name = line[1]
                    val = int(line[2])
                    info[id] = {
                        'name': name,
                        'points': val
                    }
                    name_to_id[name] = id

        return info, name_to_id
    except FileNotFoundError:
        print(f'Error: Assignment file not found at {file_path}')
        return {}, {}


def load_submissions(file_path='data/submissions.txt'):
    submission = {}
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip().split(', ')
                if len(line) == 3:
                    student = line[0]
                    assignment = line[1]
                    percentage = float(line[2])

                    if student not in submission:
                        submission[student] = {}

                    submission[student][assignment] = percentage
        return submission
    except FileNotFoundError:
        print(f'Error: Submission file not found at {file_path}')
        return {}


def calculate(name_to_id, assignment_info_by_id, submission):
    a = input("What is the student's name: ")

    if a not in name_to_id:
        print("Student not found")
        return

    student_id = name_to_id[a]
    total_points_earned = 0.0
    total_possible_points = 1000.0

    student_scores = submission.get(student_id, {})

    if not student_scores:
        print("Error: Student has no submission data.")
        return

    for assign_id, percentage in student_scores.items():
        assign_points_possible = assignment_info_by_id.get(assign_id, {}).get('points', 0)

        received_points = (percentage / 100.0) * assign_points_possible
        total_points_earned += received_points

    final_grade_percent = (total_points_earned / total_possible_points) * 100.0

    rounded_grade = round(final_grade_percent)

    print(f"{rounded_grade}%")


def analysis(assignment_name_to_id, assignment_info_by_id, submission):
    a = input("What is the assignment name: ")

    if a not in assignment_name_to_id:
        print("Assignment not found")
        return

    assign_id = assignment_name_to_id[a]

    scores = []

    for student in submission:
        if assign_id in submission[student]:
            scores.append(submission[student][assign_id])

    if not scores:
        print("No score found")
        return

    minimum = round(min(scores))
    maximum = round(max(scores))
    average = round(statistics.mean(scores))

    print(f"Min: {minimum}%, Avg: {average}%, Max: {maximum}%")


def graphed(assignment_name_to_id, assignment_info_by_id, submission):
    a = input("What is the assignment's name: ")

    if a not in assignment_name_to_id:
        print("Assignment not found")
        return

    assign_id = assignment_name_to_id[a]

    scores = []

    for student in submission:
        if assign_id in submission[student]:
            scores.append(submission[student][assign_id])

    if not scores:
        print("No score found")
        return

    bins = [0, 25, 50, 75, 100]

    plt.figure(figsize=(8, 5))

    plt.hist(scores, bins=bins, edgecolor='black', alpha=0.75)

    plt.title(f'Score Distribution of {a}', fontsize=14)
    plt.xlabel('Percentage Score', fontsize=12)
    plt.ylabel('Number of Students', fontsize=12)
    plt.xticks(bins)
    plt.grid(axis='y', alpha=0.5)

    plt.show()


def main():
    id_to_student, student_name_to_id = load_students()
    assignment_info_by_id, assignment_name_to_id = load_assignments()
    submissions = load_submissions()

    print("\n 1. Student grade")
    print(" 2. Assignment statistics")
    print(" 3. Assignment graph")
    print("-----------------------------------")

    a = input('Enter your selection: ')

    if a == '1':
        calculate(student_name_to_id, assignment_info_by_id, submissions)
    elif a == '2':
        analysis(assignment_name_to_id, assignment_info_by_id, submissions)
    elif a == '3':
        graphed(assignment_name_to_id, assignment_info_by_id, submissions)
    else:
        print('Invalid selection')


if __name__ == '__main__':
    main()