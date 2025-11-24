import random
import osmnx as ox
import networkx as nx
from datetime import datetime, timedelta

from graph import CityGraph
from planner import LogisticsPlanner

def setup_real_world_scenario(place_name="Piedmont, California, USA", num_orders=5):
    """
    Uses the heavy library 'osmnx' to download real-world street data.
    It converts the OpenStreetMap graph into our custom CityGraph.
    """
    print(f"--- 1. Downloading real map data for: {place_name} ---")
    print("    (This may take a moment depending on internet speed...)")
    
    G_osm = ox.graph_from_place(place_name, network_type='drive')
    
    print(f"    -> Downloaded {len(G_osm.nodes)} locations and {len(G_osm.edges)} road segments.")
    
    city = CityGraph()
    
    count = 0
    for u, v, data in G_osm.edges(data=True):
        distance_km = data.get('length', 100) / 1000.0
        
        city.add_road(u, v, distance_km)
        count += 1
        
    print(f"    -> Converted {count} road segments into CityGraph format.")

    all_nodes = list(G_osm.nodes())
    
    warehouse_node = random.choice(all_nodes)
    
    candidates = [n for n in all_nodes if n != warehouse_node]
    destinations = random.sample(candidates, num_orders)
    
    print(f"--- 2. Generating {num_orders} orders on real coordinates ---")
    print(f"    Warehouse Location ID: {warehouse_node}")
    
    orders = []
    base_time = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
    
    for i, dest_node in enumerate(destinations):
        start_delay = random.uniform(0.5, 4)
        window_open = base_time + timedelta(hours=start_delay)
        window_close = window_open + timedelta(hours=random.uniform(1, 3))
        
        orders.append({
            'id': i + 1,
            'destination': dest_node,
            'weight': random.randint(5, 30),
            'priority': random.randint(1, 100),
            'time_window': (window_open, window_close)
        })

    return city, orders, warehouse_node

if __name__ == "__main__":
    
    LOCATION_QUERY = "Piedmont, California, USA" 
    
    VEHICLE_CAPACITY = 100
    START_TIME = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)

    try:
        city_map, all_orders, warehouse_id = setup_real_world_scenario(
            place_name=LOCATION_QUERY,
            num_orders=10
        )

        planner = LogisticsPlanner(city_map)

        planner.create_delivery_plan(
            warehouse=warehouse_id,
            all_orders=all_orders,
            vehicle_capacity=VEHICLE_CAPACITY,
            departure_time=START_TIME
        )
