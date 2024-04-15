import random
def generate_random_points_to_file(num_points, dimension, filename):
    with open(filename, 'w') as file:
        for _ in range(num_points):
            point = tuple(round(random.randint(0, 500),6) for _ in range(dimension))
            file.write(' '.join(map(str, point)) + '\n')

def normalize_points(input_filename, output_filename):
    points = []
    with open(input_filename, 'r') as infile:
        for line in infile:
            coordinates = list(map(float, line.strip().split(' ')))
            points.append(coordinates)
    
    transposed_points = list(zip(*points))
    
    min_vals = [min(coord) for coord in transposed_points]
    max_vals = [max(coord) for coord in transposed_points]
    
    with open(output_filename, 'w') as outfile:
        for point in points:
            normalized_point = [(coord - min_val) / (max_val - min_val) for coord, min_val, max_val in zip(point, min_vals, max_vals)]
            normalized_point_rounded = [round(coord, 6) for coord in normalized_point]
            outfile.write(' '.join(map(str, normalized_point_rounded)) + '\n')

num_points = 5120
dimension = 1024
filename = '/Users/dhruvrao/Desktop/rl/data_point1.txt'
normalized_points_file = '/Users/dhruvrao/Desktop/rl/normalized_data_point1.txt'

generate_random_points_to_file(num_points, dimension, filename)
print(f"{num_points} random points of dimension {dimension} have been written to {filename}.")
normalize_points(filename, normalized_points_file)
print(f"The Normalized points of the above file have been written to {normalized_points_file}.")
