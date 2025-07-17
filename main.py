# main.py

from datetime import datetime, timedelta
import random

from graph import CityGraph
from planner import LogisticsPlanner

def setup_random_scenario():
    """
    Generates a random city map and a random list of orders.
    Returns:
        A tuple containing the city_graph and the list of orders.
    """
    print("--- Generating a new random scenario ---")
    
    # 1. Create a random city map
    city = CityGraph()
    possible_locations = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
    num_locations = random.randint(6, len(possible_locations)) # Choose 6 to 12 locations
    locations = ['Warehouse'] + random.sample(possible_locations, num_locations)
    
    # Ensure the graph is connected by linking each new location to a random existing one
    for i in range(1, len(locations)):
        loc1 = locations[i]
        loc2 = random.choice(locations[:i]) # Connect to a previously added location
        distance = random.randint(3, 15)
        city.add_road(loc1, loc2, distance)

    # Add some extra random roads to make the map more complex
    for _ in range(num_locations // 2):
        loc1, loc2 = random.sample(locations, 2)
        if loc2 not in city.edges.get(loc1, []): # Avoid duplicate roads
            distance = random.randint(3, 15)
            city.add_road(loc1, loc2, distance)

    print(f"Generated a city with {len(locations)} locations.")

    # 2. Create a random list of orders
    orders_to_deliver = []
    num_orders = random.randint(10, 20)
    # The locations that are not the warehouse are possible destinations
    possible_destinations = [loc for loc in locations if loc != 'Warehouse']

    for i in range(num_orders):
        # Generate a random time window for delivery
        start_offset_hours = random.uniform(0.5, 4.0) # Delivery can start 30 mins to 4 hours after departure
        window_duration_hours = random.uniform(1.0, 3.0) # Delivery window is 1 to 3 hours long
        
        start_time = DEPARTURE_TIME + timedelta(hours=start_offset_hours)
        end_time = start_time + timedelta(hours=window_duration_hours)

        order = {
            'id': i + 1,
            'destination': random.choice(possible_destinations),
            'weight': random.randint(5, 40),       # Weight between 5kg and 40kg
            'priority': random.randint(50, 150),   # Priority score
            'time_window': (start_time, end_time)
        }
        orders_to_deliver.append(order)
    
    print(f"Generated {len(orders_to_deliver)} random orders.")
    return city, orders_to_deliver


if __name__ == "__main__":
    
    # Define vehicle properties and departure time
    VEHICLE_CAPACITY_KG = 100
    DEPARTURE_TIME = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)

    # Generate the random city and orders for this run
    city_map, orders = setup_random_scenario()

    # Initialize our planner with the newly generated city map
    planner = LogisticsPlanner(city_map)

    # Create the delivery plan using the random data
    planner.create_delivery_plan(
        warehouse='Warehouse',
        all_orders=orders,
        vehicle_capacity=VEHICLE_CAPACITY_KG,
        departure_time=DEPARTURE_TIME
    )
