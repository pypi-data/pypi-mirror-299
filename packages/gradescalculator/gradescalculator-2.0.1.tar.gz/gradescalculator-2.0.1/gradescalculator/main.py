import argparse
import csv
import sys
from math import prod

def calculate_grades(grades, method='weighted'):
    if method == 'weighted':
        # Calculate the total weighted sum and total weight
        total_weighted_sum = sum(item["weight"] * item["grade"] for item in grades.values())
        total_weight = sum(item["weight"] for item in grades.values())

        # Check if total weight is zero to avoid division by zero
        if total_weight == 0:
            raise ValueError("Total weight must be greater than zero.")

        # Calculate the weighted average
        overall_grade = total_weighted_sum / total_weight
    elif method == 'arithmetic':
        # Calculate the arithmetic mean
        overall_grade = sum(item["grade"] for item in grades.values()) / len(grades)
    elif method == 'geometric':
        # Calculate the geometric mean
        overall_grade = prod(item["grade"] for item in grades.values()) ** (1 / len(grades))
    else:
        raise ValueError("Unsupported calculation method.")

    # Round the overall grade to the nearest 0.01 and 0.5
    precise_overall_grade = round(overall_grade * 100) / 100
    rounded_overall_grade = round(overall_grade * 2) / 2

    return precise_overall_grade, rounded_overall_grade

def read_grades_from_csv(file_path):
    grades = {}
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for i, row in enumerate(reader):
            if len(row) != 2:
                raise ValueError(f"Incorrect number of columns in row {i+1}")
            grade, weight = map(float, row)
            grades[f'grade {i+1}'] = {"weight": weight, "grade": grade}
    return grades

def main():
    parser = argparse.ArgumentParser(description="Calcule la note globale à partir des notes.")
    parser.add_argument('--csv', type=str, help='Chemin vers le fichier CSV contenant les notes et leurs poids.')
    parser.add_argument('--method', type=str, choices=['weighted', 'arithmetic', 'geometric'], default='weighted', help='Méthode de calcul de la note globale.')
    parser.add_argument('grades', metavar='N', type=float, nargs='*', help='Liste des notes et de leurs poids sous la forme: note1 poids1 note2 poids2 ...')
    args = parser.parse_args()

    if args.csv:
        # Read grades from the CSV file
        grades = read_grades_from_csv(args.csv)
    else:
        # Ensure the number of grades and weights is even
        if len(args.grades) % 2 != 0:
            raise ValueError("Le nombre de valeurs pour les notes et les poids doit être pair.")

        # Convert the grades and weights to a dictionary
        grades = {}
        for i in range(0, len(args.grades), 2):
            grades[f'grade {i//2 + 1}'] = {"weight": args.grades[i+1], "grade": args.grades[i]}

    # Calculate the overall grade
    precise_grade, rounded_grade = calculate_grades(grades, method=args.method)
    
    # Print the results
    print(f"Precise Overall Grade (rounded to the nearest 0.01): {precise_grade}")
    print(f"Rounded Overall Grade (rounded to the nearest 0.5): {rounded_grade}")

if __name__ == '__main__':
    main()
