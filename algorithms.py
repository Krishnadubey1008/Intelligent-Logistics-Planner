# algorithms.py

import sys
from datetime import timedelta

def select_best_packages(all_orders, vehicle_capacity):
    """
    Chooses the best set of packages to fit in the vehicle.
    It maximizes the total priority of packages without exceeding the vehicle's
    weight capacity. This is a classic optimization problem called the
    "0/1 Knapsack Problem".
    """
    num_orders = len(all_orders)
    
    # Create a table to help us make the decision.
    # Rows represent orders, and columns represent available weight capacity.
    # The value in each cell will be the max priority we can get.
    max_priority_table = [[0 for _ in range(vehicle_capacity + 1)] for _ in range(num_orders + 1)]

    # Go through each order and each possible weight capacity
    for i in range(1, num_orders + 1):
        order = all_orders[i-1]
        order_weight = order['weight']
        order_priority = order['priority']

        for capacity in range(1, vehicle_capacity + 1):
            if order_weight > capacity:
                # If the current order is heavier than the available capacity,
                # we can't include it. So, the max priority is the same as before.
                max_priority_table[i][capacity] = max_priority_table[i-1][capacity]
            else:
                # If the order fits, we have two choices:
                # 1. Don't include the order.
                priority_without_order = max_priority_table[i-1][capacity]
                # 2. Include the order.
                priority_with_order = order_priority + max_priority_table[i-1][capacity - order_weight]
                
                # We choose the option that gives us a higher total priority.
                max_priority_table[i][capacity] = max(priority_without_order, priority_with_order)

    # Now, backtrack through the table to find which packages we selected.
    selected_orders = []
    remaining_capacity = vehicle_capacity
    for i in range(num_orders, 0, -1):
        # If the priority changed, it means we included the item at this step.
        if max_priority_table[i][remaining_capacity] != max_priority_table[i-1][remaining_capacity]:
            order_to_add = all_orders[i-1]
            selected_orders.append(order_to_add)
            remaining_capacity -= order_to_add['weight']
            
    return selected_orders


def find_best_route(start_location, orders_to_deliver, distance_matrix, departure_time):
    """
    Determines the best order to visit destinations, respecting delivery time windows.
    This uses a "greedy" approach: at each step, it picks the next stop that is
    quickest to get to (including any waiting time).
    """
    # Use an average speed to convert distance (km) to travel time.
    AVG_SPEED_KMH = 40
    
    route = [start_location]
    itinerary = []
    current_time = departure_time
    total_distance = 0
    current_location = start_location
    
    unvisited_orders = list(orders_to_deliver)

    while unvisited_orders:
        best_next_order = None
        # A simple cost: how long will it take to get to the next stop and finish?
        # We want to minimize this time.
        min_time_to_next_stop = sys.maxsize 

        for order in unvisited_orders:
            destination = order['destination']
            travel_distance = distance_matrix[current_location][destination]
            travel_time = timedelta(hours=travel_distance / AVG_SPEED_KMH)
            arrival_time = current_time + travel_time

            # If we arrive after the delivery window is closed, we can't visit this stop next.
            if arrival_time > order['time_window'][1]:
                continue 

            # If we arrive before the window opens, we have to wait.
            wait_time = max(timedelta(0), order['time_window'][0] - arrival_time)
            
            total_time_cost = travel_time + wait_time

            if total_time_cost.total_seconds() < min_time_to_next_stop:
                min_time_to_next_stop = total_time_cost.total_seconds()
                best_next_order = order
        
        if best_next_order is None:
            # This happens if no remaining orders can be visited in their time windows.
            print("Warning: Could not find a valid next stop. Ending route here.")
            break

        # Update our route and time after visiting the best next stop.
        travel_dist = distance_matrix[current_location][best_next_order['destination']]
        travel_time = timedelta(hours=travel_dist/AVG_SPEED_KMH)
        arrival_time = current_time + travel_time
        wait_time = max(timedelta(0), best_next_order['time_window'][0] - arrival_time)
        
        current_location = best_next_order['destination']
        current_time = arrival_time + wait_time + timedelta(minutes=10) # Add 10 mins for drop-off
        total_distance += travel_dist
        
        route.append(current_location)
        itinerary.append({'order_id': best_next_order['id'], 'location': current_location, 'arrival_time': arrival_time + wait_time})
        unvisited_orders.remove(best_next_order)

    # Finally, add the return trip to the warehouse.
    route.append(start_location)
    total_distance += distance_matrix[current_location][start_location]

    return route, itinerary, total_distance
