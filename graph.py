# graph.py

import heapq
import sys

class CityGraph:
    """
    Represents the city map as a graph.
    - Nodes are locations (e.g., 'Warehouse', 'A', 'B').
    - Edges are the roads connecting locations, with a distance.
    """
    def __init__(self):
        self.nodes = set()
        self.edges = {}
        self.distances = {}

    def add_road(self, from_location, to_location, distance):
        """Adds a two-way road between two locations."""
        self.nodes.add(from_location)
        self.nodes.add(to_location)

        if from_location not in self.edges:
            self.edges[from_location] = []
        if to_location not in self.edges:
            self.edges[to_location] = []

        self.edges[from_location].append(to_location)
        self.edges[to_location].append(from_location)

        self.distances[(from_location, to_location)] = distance
        self.distances[(to_location, from_location)] = distance

    def find_shortest_path(self, start_location):
        """
        Calculates the shortest distance from a starting location to all others.
        This function uses Dijkstra's algorithm.
        """
        distances = {node: sys.maxsize for node in self.nodes}
        distances[start_location] = 0
        locations_to_visit = [(0, start_location)]

        while locations_to_visit:
            current_distance, current_location = heapq.heappop(locations_to_visit)

            if current_distance > distances[current_location]:
                continue

            for neighbor in self.edges.get(current_location, []):
                road_distance = self.distances[(current_location, neighbor)]
                new_distance_to_neighbor = current_distance + road_distance

                if new_distance_to_neighbor < distances[neighbor]:
                    distances[neighbor] = new_distance_to_neighbor
                    heapq.heappush(locations_to_visit, (new_distance_to_neighbor, neighbor))

        return distances
