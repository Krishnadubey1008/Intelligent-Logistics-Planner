from graph import CityGraph
from algorithms import select_best_packages, find_best_route

class LogisticsPlanner:
    def __init__(self, city_graph: CityGraph):
        self.graph = city_graph
        self.distance_matrix = self._create_distance_matrix()

    def _create_distance_matrix(self):
        print("Calculating all distances between locations...")
        matrix = {}
        for location in self.graph.nodes:
            matrix[location] = self.graph.find_shortest_path(location)
        print("...distance calculations complete.")
        return matrix

    def create_delivery_plan(self, warehouse, all_orders, vehicle_capacity, departure_time):
        print("\n--- Starting New Delivery Plan ---")
        
        print(f"\n1. Selecting packages (Vehicle Capacity: {vehicle_capacity}kg)...")
        selected_orders = select_best_packages(all_orders, vehicle_capacity)
        
        if not selected_orders:
            print("No orders could be selected. The vehicle may have too little capacity.")
            return

        print(f"Selected {len(selected_orders)} out of {len(all_orders)} orders:")
        for order in selected_orders:
            print(f"  - Order {order['id']} to {order['destination']} ({order['weight']}kg)")

        print("\n2. Calculating the best route...")
        route, itinerary, total_distance = find_best_route(
            warehouse, selected_orders, self.distance_matrix, departure_time
        )

        print("\n--- Final Delivery Itinerary ---")
        if not route:
            print("A valid route could not be generated.")
            return
            
        print(f"Total estimated distance for the route: {total_distance:.1f} km")
        print("Route sequence:")
        print(" -> ".join(route))
        
        print("\nStep-by-step plan:")
        print(f"  - {departure_time:%H:%M}: Depart from {warehouse}")
        for stop in itinerary:
            print(f"  - {stop['arrival_time']:%H:%M}: Arrive at {stop['location']} for order {stop['order_id']}")
        print("  - Return to Warehouse")
        print("--- Plan Complete ---")
