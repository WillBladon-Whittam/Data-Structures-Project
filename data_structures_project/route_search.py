import heapq
from typing import Dict


def heuristic(start, end, heuristic_values):
    """
    Returns the heuristic straight-line distance from a specific node
    """
    if start == end:
        return 0
    return heuristic_values[start][end]


def route_search(graph: Dict[str, Dict[str, int]], start: str, end: str, a_star_heuristics: None | Dict[str, Dict[str, int]] = None):
    """
    This function finds the shortest path between 2 locations.
    The algorithm used by default is dijkstra, but A* can be used if a set of heuristic values are specified

    Args:
        graph: A graph containing the nodes and vertices to search
        start: The node to start from in the graph 
        end: The node to end on in the graph
        a_star_heuristics: If set to None, use dijkstra (default).
                           Otherwise contains heuristic values to use the A* algorithm

    Returns:
        Path used to get to the destination and the distance travelled
    """
    queue = [(0, 0, start)]
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    previous_nodes = {node: None for node in graph}

    while queue:
        priority, current_distance, current_node = heapq.heappop(queue)

        # If the current node is the destination, we are done
        if current_node == end:
            break

        # If a shorter path to the current node has been found, skip this one
        if current_distance > distances[current_node]:
            continue

        # Explore neighbors
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight

            # If a shorter path to the neighbor is found
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                priority = distance + (heuristic(neighbor, end, a_star_heuristics) if a_star_heuristics is not None else 0)
                heapq.heappush(queue, (priority, distance, neighbor))

    # Reconstruct the shortest path
    path = []
    current_node = end
    while previous_nodes[current_node] is not None:
        path.insert(0, current_node)
        current_node = previous_nodes[current_node]
    if path:
        path.insert(0, current_node)

    return path, distances[end]


if __name__ == "__main__":
    start = 'Park'
    end = 'Cinema'

    # Test data
    graph = {
        'Park': {'Train Station': 42, 'Library': 87},
        'Train Station': {'Park': 42, 'Library': 94, 'School': 51, 'Museum': 36},
        'Library': {'Park': 87, 'Train Station': 94, 'School': 28, 'Cinema': 85},
        'School': {'Train Station': 51, 'Library': 28, 'Cinema': 39},
        'Museum': {'Train Station': 36, 'Cinema': 99},
        'Cinema': {'Library': 85, 'School': 39, 'Museum': 99}
    }

    heuristic_values = {
        'Park': {'Train Station': 40, 'Library': 80, 'School': 90, 'Museum': 50, 'Cinema': 90},
        'Train Station': {'Park': 40, 'Library': 60, 'School': 50, 'Museum': 35, 'Cinema': 80},
        'Library': {'Park': 80, 'Train Station': 60, 'School': 20, 'Museum': 70, 'Cinema': 70},
        'School': {'Park': 90, 'Train Station': 50, 'Library': 20, 'Museum': 60, 'Cinema': 40},
        'Museum': {'Park': 50, 'Train Station': 35, 'Library': 70, 'School': 60, 'Cinema': 60},
        'Cinema': {'Park': 90, 'Train Station': 80, 'Library': 70, 'School': 40, 'Museum': 60}
    }

    shortest_path, distance = route_search(
        graph, start, end, a_star_heuristics=heuristic_values)
    print(f"Shortest path from {start} to {
          end} using A*: {shortest_path} with distance {distance}")

    shortest_path, distance = route_search(graph, start, end)
    print(f"Shortest path from {start} to {end} using Dijkstra: {
          shortest_path} with distance {distance}")
