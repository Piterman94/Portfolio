import math
import csv
from typing import Dict, List, Tuple, Set
from scipy.spatial import distance_matrix
from scipy.optimize import linear_sum_assignment

# Calculate distance between two sets of coordinates
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of the Earth in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) * \
        math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

# Load employee addresses from CSV file
employee_addresses = []
with open('employee_addresses.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip header row
    for row in reader:
        address = row[0]
        employee_addresses.append(address)

# Load store addresses from CSV file
store_addresses = []
with open('store_addresses.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip header row
    for row in reader:
        address = row[0]
        store_addresses.append(address)

# Calculate distance matrix between employees and stores
def calculate_distance_matrix():
    employee_coords = [tuple(map(float, address.split(", "))) for address in employee_addresses]
    store_coords = [tuple(map(float, address.split(", "))) for address in store_addresses]

    # Calculate the distance matrix using the haversine distance between each pair of points
    dist_matrix = distance_matrix(employee_coords, store_coords, p=2) * 6371  # Radius of the Earth

    return dist_matrix


def print_distance_matrix(dist_matrix):
    num_employees = len(employee_addresses)
    num_stores = len(store_addresses)

    # Print the matrix header
    print(f"{'':<20}", end="")
    for j in range(num_stores):
        print(f"Store {j+1:<7}", end="")
    print()

    # Print each row of the matrix
    for i in range(num_employees):
        print(f"Employee {i+1:<4}", end="")
        for j in range(num_stores):
            print(f"{dist_matrix[i, j]:<7.2f}", end="")
        print()

# Save the matrix to CSV file
    with open('distance_matrix.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        header = [''] + [f'Store {j+1}' for j in range(num_stores)]
        writer.writerow(header)
        for i in range(num_employees):
            row = [f'Employee {i+1}'] + [dist_matrix[i, j] for j in range(num_stores)]
            writer.writerow(row)

if __name__ == "__main__":
    dist_matrix = calculate_distance_matrix()
    print_distance_matrix(dist_matrix)