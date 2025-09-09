import sys
import os
import csv
import random
from collections import defaultdict

def create_full_database(default_path = 'data/db/full_database.csv', objs_path = 'data/shape-database'):
    shapes = []
    os.makedirs(os.path.dirname(default_path), exist_ok=True)

    for root, dirs, files in os.walk(objs_path):
        shape_class = os.path.basename(root)
        #print(shape_class)

        for file in files:
            file_path = os.path.join(root, file)
            vertices, faces, triangles, quads = count_vertices_and_faces(file_path)
            shapes.append([file, shape_class, vertices, faces, triangles, quads])

        # shapes.sort(key=lambda x: x[0]) # keep alphabetical order?

    write_rows(default_path, shapes)

def create_reduced_database(nr_shapes = 200, default_path = 'data/db/reduced_database.csv', objs_path = 'data/shape-database'):
    # at least 200 shapes
    shapes = defaultdict(list)
    os.makedirs(os.path.dirname(default_path), exist_ok=True)

    for root, dirs, files in os.walk(objs_path):
        shape_class = os.path.basename(root)
        #print(shape_class)

        for file in files:
            file_path = os.path.join(root, file)
            vertices, faces, triangles, quads = count_vertices_and_faces(file_path)
            shapes[shape_class].append([file, shape_class, vertices, faces, triangles, quads])
    
    total_available = sum(len(l) for l in shapes.values())
    nr_classes = len(shapes)

    if nr_shapes >= total_available:
        # use all of them
        chosen_shapes = [s for lst in shapes.values() for s in lst]
    else:
        per_class = nr_shapes // nr_classes
        chosen_shapes = []
        remaining = nr_shapes

        for k, l in shapes.items():
            max_class_samples = min(per_class, len(l))
            sampled = random.sample(l, max_class_samples)
            chosen_shapes.extend(sampled)
            remaining -= len(sampled)

        if remaining > 0:
            leftovers = []

            for k, l in shapes.items():
                already_taken = [s for s in chosen_shapes if s[0] == k]
                remaining_shapes = [s for s in l if s not in already_taken]
                leftovers.extend(remaining_shapes)

            extra_samples = random.sample(leftovers, remaining)
            chosen_shapes.extend(extra_samples)

    write_rows(default_path, chosen_shapes)

def add_model(file_path, db_path = 'data/db/full_database.csv'):
    shape_class = os.path.basename(os.path.dirname(file_path))
    vertices, faces, triangles, quads = count_vertices_and_faces(file_path)
    
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    if not os.path.exists(db_path):
        with open(db_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Shape class", "Nr vertices", "Nr faces", "Nr triangles", "Nr quads"])

    with open(db_path, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([os.path.basename(file_path), shape_class, vertices, faces, triangles, quads])

def write_rows(default_path, shapes):
    with open(default_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Shape class", "Nr vertices", "Nr faces", "Nr triangles", "Nr quads"])
        writer.writerows(shapes)

    print(f"New CSV file created at: {default_path}")

def count_vertices_and_faces(file_path):
    vertices, faces, triangles, quads = 0, 0, 0, 0
    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            if line.startswith("v "):
                vertices += 1
            elif line.startswith("f "):
                faces += 1

                x = line.split()
                if(len(x) == 4):
                    triangles += 1
                elif(len(x) == 5):
                    quads += 1

    return vertices, faces, triangles, quads