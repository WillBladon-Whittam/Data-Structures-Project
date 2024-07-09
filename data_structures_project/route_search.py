import heapq
from heapq import heappush, heappop


def dijkstra(graph, start, end):
    # Priority queue to store (distance, node) tuples
    queue = [(0, start)]
    # Dictionary to store the shortest path to each node
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    # Dictionary to store the previous node in the optimal path
    previous_nodes = {node: None for node in graph}
    
    while queue:
        current_distance, current_node = heapq.heappop(queue)
        
        # If the current node is the destination, we're done
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
                heapq.heappush(queue, (distance, neighbor))
    
    # Reconstruct the shortest path
    path = []
    current_node = end
    while previous_nodes[current_node] is not None:
        path.insert(0, current_node)
        current_node = previous_nodes[current_node]
    if path:
        path.insert(0, current_node)
    
    return path


if __name__ == "__main__":
    graph = {
        "B": {"A": 5, "D": 1, "G": 2}, 
        "A": {"B": 5, "D": 3, "E": 12, "F": 5}, 
        "D": {"B": 1, "G": 1, "E": 1, "A": 3}, 
        "G": {"B": 2, "D": 1, "C": 2}, 
        "C": {"G": 2, "E": 1, "F": 16}, 
        "E": {"A": 12, "D": 1, "C": 1, "F": 2}, 
        "F": {"A": 5, "E": 2, "C": 16}
        }
    print(dijkstra(graph, "B", "E"))
