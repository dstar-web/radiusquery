import math
import random
import time

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def __repr__(self):
        current = self.head
        nodes = []
        while current:
            nodes.append(current.data)
            current = current.next
        return ' -> '.join(map(str, nodes))

def read_points_from_file(filename):
    points = []
    with open(filename, 'r') as file:
        for line in file:
            coordinates = list(map(float, line.strip().split(' ')))
            points.append(tuple(coordinates))
    return points

def append_query_points(query_filename, normalized_points):
    query_points = read_points_from_file(query_filename)
    start_index = len(normalized_points)  
    normalized_points.extend(query_points)
    return list(range(start_index, len(normalized_points)))  

def choose_reference_point(points):
    return random.choice(points)

def distance(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))

def radius_query(points, radius, reference, query_indices):
    dist = []
    length_X = len(points)
    for i in range(length_X):
        d = round(distance(reference, points[i]), 1)
        dist.append(d)
    
    sorted_X_indices = [i for i, _ in sorted(enumerate(dist), key=lambda x: x[1])]
    sorted_X = [points[i] for i in sorted_X_indices]

    hash_table = {}

    for i in sorted_X_indices:
        hash_table[i] = LinkedList()

    for i in range(length_X):
        for j in range(i + 1, length_X):
            if distance(reference, sorted_X[j]) - distance(reference, sorted_X[i]) > radius:
                break
            if distance(sorted_X[i], sorted_X[j]) <= radius:
                hash_table[sorted_X_indices[i]].append(sorted_X_indices[j])
                hash_table[sorted_X_indices[j]].append(sorted_X_indices[i])

    return {key: hash_table[key] for key in query_indices}


def write_result_to_file(hash_table, filename):
    with open(filename, 'w') as file:
        file.write("===============================================================\n")
        i=0
        for key, value in hash_table.items():
            file.write(f"Result[{i}]: {value}\n") 
            i+=1

if __name__ == "__main__":
    normalized_points_filename = "lsh_normalized_points.txt"
    query_filename = "lsh_query_points.txt"
    radius = 0.6
    
    normalized_points = read_points_from_file(normalized_points_filename)
    query_points = read_points_from_file(query_filename)
    print(f"The total number of Given data points are: {len(normalized_points)}")
    print(f"The total number of Query Points are: {len(query_points)}")
    print(f"The dimensions of the points is: {len(normalized_points[0])}")
    print(f"The given radius is: {radius}")
    query_indices = append_query_points(query_filename, normalized_points)
    print(f"The total number of processing points after appending query points are: {len(normalized_points)}")

    reference = choose_reference_point(normalized_points)
    
    start_time = time.time()
    hash_table = radius_query(normalized_points, radius, reference, query_indices)
    end_time = time.time()

    result_filename = "result.txt"
    write_result_to_file(hash_table, result_filename)
    print(f"Result is available in \"{result_filename}\" file.")
    print("========================================================")
    print(f"The time taken is {end_time - start_time} seconds.")