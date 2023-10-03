import math
import csv
import random
from typing import Dict, List, Tuple

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

# Employee allocation function
def allocate_employees(employee_addresses, store_addresses):
    employee_allocation: Dict[str, List[Tuple[str, float]]] = {}
    total_distance: float = 0.0

    # Track the number of employees allocated to each store
    allocated_employees_per_store = {store: 0 for store in store_addresses}

    for employee_address in employee_addresses:
        employee_lat, employee_lon = map(float, employee_address.split(", "))
        closest_store = None
        min_distance = math.inf

        for store_address in store_addresses:
            if allocated_employees_per_store[store_address] < 1000:  # Limit to 1000 employees per store
                store_lat, store_lon = map(float, store_address.split(", "))
                distance = calculate_distance(employee_lat, employee_lon, store_lat, store_lon)
                if distance < min_distance:
                    closest_store = store_address
                    min_distance = distance

        if closest_store is not None:
            if closest_store in employee_allocation:
                employee_allocation[closest_store].append((employee_address, min_distance))
            else:
                employee_allocation[closest_store] = [(employee_address, min_distance)]

            total_distance += min_distance
            allocated_employees_per_store[closest_store] += 1

    return employee_allocation, total_distance

# Main function
def main():
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

    # Number of iterations to run
    num_iterations = 10000
    best_total_distance = math.inf
    worst_total_distance = 0.0
    best_employee_allocation = None

    for i in range(num_iterations):
        random.shuffle(employee_addresses)  # Shuffle employees to allocate differently each time
        employee_allocation, total_distance = allocate_employees(employee_addresses, store_addresses)

        # Update the best and worst solutions
        if total_distance < best_total_distance:
            best_total_distance = total_distance
            best_employee_allocation = employee_allocation

        if total_distance > worst_total_distance:
            worst_total_distance = total_distance

    print(f"Total Distance for the Best Solution: {best_total_distance:.2f} km")
    print(f"Total Distance for the Worst Solution: {worst_total_distance:.2f} km")
    print(f"Difference between Best and Worst Solutions: {worst_total_distance - best_total_distance:.2f} km")

    # Write the best allocation results to CSV file
    # with open('best_employee_allocation_result.csv', 'w', newline='') as csvfile:
    #     writer = csv.writer(csvfile)
    #     writer.writerow(['Store Address', 'Employee Address', 'Distance (km)'])
    #     for store_address, employees in best_employee_allocation.items():
    #         for employee_address, distance in employees:
    #             writer.writerow([store_address, employee_address, distance])

if __name__ == "__main__":
    main()
