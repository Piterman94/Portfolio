import math
import csv
from typing import Dict, List, Tuple
from scipy.spatial import distance_matrix

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

# Allocate employees to stores
def allocate_employees_to_stores(dist_matrix):
    num_employees, num_stores = dist_matrix.shape

    # Create a list to keep track of the best employees for each store
    best_employees_for_store = [[] for _ in range(num_stores)]

    # Find the best 200 employees for each store
    for employee_idx in range(num_employees):
        best_store = None
        min_distance = float('inf')

        for store_idx in range(num_stores):
            distance = dist_matrix[employee_idx, store_idx]
            if distance < min_distance and len(best_employees_for_store[store_idx]) < 200:
                best_store = store_idx
                min_distance = distance

        if best_store is not None:
            best_employees_for_store[best_store].append((employee_idx, min_distance))

    # Convert the best employees list to the required format
    employee_allocation = {}
    for store_idx, employees in enumerate(best_employees_for_store):
        store_address = store_addresses[store_idx]
        employee_allocation[store_address] = [(employee_addresses[idx], distance) for idx, distance in employees]

    return employee_allocation

# Write employee coordinates and assigned stores to CSV file
def write_employee_allocation_to_csv(employee_allocation):
    with open('employee_allocation.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Employee Address', 'Store Address', 'Distance (km)'])
        for store_address, employees in employee_allocation.items():
            for employee_address, distance in employees:
                writer.writerow([employee_address, store_address, distance])

# Main function
def main():
    dist_matrix = calculate_distance_matrix()
    employee_allocation = allocate_employees_to_stores(dist_matrix)

    # Print employee allocation results
    for store_address, employees in employee_allocation.items():
        print(f"Store Address: {store_address}")
        for employee_address, distance in employees:
            print(f"  - Employee Address: {employee_address}")
            print(f"    Distance: {distance:.2f} km")

    # Write employee allocation to CSV
    write_employee_allocation_to_csv(employee_allocation)

if __name__ == "__main__":
    main()

