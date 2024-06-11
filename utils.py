from typing import Tuple, List

def prompt_number(prompt: str, _range: Tuple[int, int | None] = None,
                    error_message: str = "Invalid Value!") -> int:
    """
    Prompts the user for a number between a specific range.
    """
    selected_option = -1
    if _range is None:  # If no range is specified
        while not selected_option > 0:
            try:
                selected_option = int(input(prompt))
            except ValueError:
                print(f"{error_message}\n")
                continue
            if selected_option <= 0:
                print(f"{error_message}\n")
        return selected_option
    elif _range[1] is None:  # If there is a minimum value
        while not _range[0] <= selected_option:
            try:
                selected_option = int(input(prompt))
            except ValueError:
                print(f"{error_message}\n")
                continue
            if selected_option <= _range[0]:
                print(f"{error_message}\n")
    else:  # If there is a range of 2 values
        while selected_option not in range(_range[0], _range[1] + 1):
            try:
                selected_option = int(input(prompt))
            except ValueError:
                print(f"{error_message}\n")
                continue
            if selected_option not in range(_range[0], _range[1] + 1):
                print(f"{error_message}\n")
    return selected_option
    
def display_options(options: List[str]) -> None:
    """
    Displays the options given in an ordered list
    """
    for i, option in enumerate(options, start=1):
        split_option = str(option).split("\n")
        print(f"{i}.\t{split_option[0]}")
        for line in split_option[1:]:
            print(f"  \t{line}")
        