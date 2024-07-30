from typing import Tuple, List, Union, Dict
import datetime
import heapq


def prompt_number(prompt: str, _range: Tuple[int | None, int | None] | None = None,
                  error_message: str = "Invalid Value!") -> int:
    """
    Prompts for a valid number

    Args:
        prompt: Prompt displayed before entering the number
        _range: Can specify a min and/or max number to be required
        error_message: Specify the error message to be displayed
    """
    while True:
        try:
            selected_option = int(input(prompt))
            if (_range is None and selected_option > 0) or \
               (_range is not None and (_range[0] is None or selected_option >= _range[0]) and 
                (_range[1] is None or selected_option <= _range[1])):
                return selected_option
            else:
                print(f"{error_message}\n")
        except ValueError:
            print(f"{error_message}\n")


def prompt_date(prompt: str, _range: Tuple[datetime.date | None, datetime.date | None] | None = None,
                error_message: str = "Invalid Date!") -> datetime.date:
    """
    Prompts for a valid date

    Args:
        prompt: Prompt displayed before entering the date
        _range: Can specify a min and/or max date to be required
        error_message: Specify the error message to be displayed
    """
    while True:
        try:
            date_input = input(prompt)
            day, month, year = map(int, date_input.split('-'))
            date = datetime.date(year, month, day)
            if (_range is None) or \
               (_range[0] is None or date >= _range[0]) and \
               (_range[1] is None or date <= _range[1]):
                return date
            else:
                print(f"{error_message}\n")
        except ValueError:
            print(f"{error_message}\n")
        
        
def prompt_yes_no(prompt: str) -> bool:
    """
    Prompts the user for a Y/N response
    """
    while True:
        selected_option = input(prompt).strip().upper()
        if selected_option in ["Y", "N"]:
            return selected_option == "Y"
        print("Please enter Y/N\n")


def display_options(options: List[str], empty_prompt: str = "List is empty!") -> None:
    """
    Displays the options given in an ordered list
    """
    if not options:
        print(empty_prompt)
        return
    for i, option in enumerate(options, start=1):
        split_option = str(option).split("\n")
        print(f"{i}.\t{split_option[0]}")
        for line in split_option[1:]:
            print(f"  \t{line}")
            
            
def quick_sort(array):
    """
    An implementation of quick sort.
    """
    if len(array) <= 1:
        return array
    
    pivot = array[len(array) // 2]
    left = [x for x in array if x < pivot]
    middle = [x for x in array if x == pivot]
    right = [x for x in array if x > pivot]
    
    return quick_sort(left) + middle + quick_sort(right)
 
 
def boyer_moore_search(text, pattern):
    """
    An implementation of the Boyer-Moore string search algorithm.
    """
    pattern_length = len(pattern)
    text_length = len(text)
    
    if pattern_length == 0:
        return False
    if pattern_length > text_length:
        return False

    last_occurrence = {}

    for index in range(pattern_length):
        last_occurrence[pattern[index]] = index
        
    shift = 0
    while shift <= text_length - pattern_length:
        match_index = pattern_length - 1

        while match_index >= 0 and pattern[match_index] == text[shift + match_index]:
            match_index -= 1

        if match_index < 0:
            return True
        else:
            char_last_occurrence = last_occurrence.get(text[shift + match_index], -1)
            shift += max(1, match_index - char_last_occurrence)

    return False
            
            
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
