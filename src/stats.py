import os
import argparse
import csv
import numpy as np
import matplotlib.pyplot as plt
from display import display_model_from_file

def run_stats_analysis(db_path = 'data/db/reduced_database.csv', nr_of_examples = 3):
    # read database file
    entries = []

    with open(db_path, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            entry = DBEntry(
                row['Name'], row['Shape class'], row['Nr vertices'], row['Nr faces'], 
                row['Nr triangles'], row['Nr quads']
            )
            entries.append(entry)

    # find avg shape in the db
    vertices_list = [e.nr_vertices for e in entries]
    faces_list = [e.nr_faces for e in entries]

    shape_classes = [e.shape_class for e in entries]
    unique_classes, counts = np.unique(shape_classes, return_counts=True)
    print(counts)

    plt.hist(counts, bins=np.arange(min(counts), max(counts)+2, 1))
    plt.title("Histogram of per class shape distribution")
    plt.xlabel("Number of items in class")
    plt.ylabel("Number of classes")
    plt.tight_layout()
    plt.show()

    plt.hist(vertices_list, bins=20)
    plt.title("Histogram of vertex counts")
    plt.xlabel("Number of vertices")
    plt.ylabel("Number of shapes")
    plt.show()

    plt.hist(faces_list, bins=20)
    plt.title("Histogram of face counts")
    plt.xlabel("Number of faces")
    plt.ylabel("Number of shapes")
    plt.show()

    avg_vertices = np.mean(vertices_list)
    avg_faces = np.mean(faces_list)

    std_v = np.std(vertices_list)
    std_f = np.std(faces_list)

    print(f"The average number of vertices is {avg_vertices}")
    print(f"The average number of faces is {avg_faces}")

    for e in entries:
        e.dist_from_avg = abs(e.nr_vertices - avg_vertices) + abs(e.nr_faces - avg_faces)

    entries_sorted = sorted(entries, key=lambda e: e.dist_from_avg)

    for x in entries_sorted[:nr_of_examples]:
        print(x.name, x.shape_class, x.nr_vertices, x.nr_faces, x.nr_triangles, x.nr_quads)
        file_path = os.path.join('data/shape-database', x.shape_class, x.name)
        display_model_from_file(file_path)

    # find outliers
    outliers = [e for e in entries if abs(e.nr_vertices - avg_vertices) > 2*std_v 
                                      or abs(e.nr_faces - avg_faces) > 2*std_f]
    
    print(f"\nFound {len(outliers)} outliers")
    
    for x in outliers[:nr_of_examples]:
        print(x.name, x.shape_class, x.nr_vertices, x.nr_faces, x.nr_triangles, x.nr_quads)
        file_path = os.path.join('data/shape-database', x.shape_class, x.name)
        display_model_from_file(file_path)

class DBEntry:
    def __init__(self, name, shape_class, nr_vertices, nr_faces, nr_triangles, nr_quads):
        self.name = name
        self.shape_class = shape_class
        self.nr_vertices = int(nr_vertices)
        self.nr_faces = int(nr_faces)
        self.nr_triangles = int(nr_triangles)
        self.nr_quads = int(nr_quads)
        self.dist_from_avg = None

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run a simple statis analysis on the database")
    
    parser.add_argument('--db_path', type=str, default='data/db/reduced_database.csv',
                        help='Path to the database CSV file')
    parser.add_argument('--nr_of_examples', type=int, default=3,
                        help='Number of examples shapes to show with vedo')

    args = parser.parse_args()

    run_stats_analysis(db_path=args.db_path, nr_of_examples=args.nr_of_examples)