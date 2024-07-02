from typing import Tuple, List, Union
import datetime


def prompt_number(prompt: str, _range: Tuple[int, int | None] = None, error_message: str = "Invalid Value!") -> int:
    """
    Prompts for a valid number

    Args:
        prompt: Prompt displayed before entering the number
        _range: Can specify a min and/or max number to be required
        error_message: Specify the error message to be displayed
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


def prompt_date(prompt: str, _range: Tuple[datetime.date, Union[datetime.date, None]] = None, error_message: str = "Invalid Date!") -> datetime.date:
    """
    Prompts for a valid date

    Args:
        prompt: Prompt displayed before entering the date
        _range: Can specify a min and/or max date to be required
        error_message: Specify the error message to be displayed
    """
    date = datetime.date(1, 1, 1)
    if _range is None:  # If no range is specified
        while True:
            try:
                date_input = input(prompt)  # validate this
                day, month, year = map(int, date_input.split('-'))
                date = datetime.date(year=year, month=month, day=day)
                return date
            except ValueError:
                print(f"{error_message}\n")
    elif _range[1] is None:  # If there is a minimum value
        while True:
            try:
                date_input = input(prompt)
                day, month, year = map(int, date_input.split('-'))
                date = datetime.date(year=year, month=month, day=day)
            except ValueError:
                print(f"{error_message}\n")
                continue
            if date <= _range[0]:
                print(f"{error_message}\n")
                continue
            return date
    else:  # If there is a range of 2 values
        while True:
            try:
                date_input = input(prompt)
                day, month, year = map(int, date_input.split('-'))
                date = datetime.date(year=year, month=month, day=day)
            except ValueError:
                print(f"{error_message}\n")
                continue
            if not _range[0] <= date <= _range[1]:
                print(f"{error_message}\n")
                continue
            return date
        
        
def prompt_yes_no(prompt: str) -> bool:
        """
        Prompts the user for a Y/N response
        """
        selected_option = None
        while selected_option not in ["Y", "N", "y", "n"]:
            selected_option = input(prompt)
            if selected_option not in ["Y", "N", "y", "n"]:
                print("Please enter Y/N\n")
        if selected_option.upper() == "Y":
            return True
        elif selected_option.upper() == "N":
            return False


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
    
    Time Complexity:
    - Best Case: O(n log n)
    - Average Vase: O(n log n)
    - Worst Case: O(n^2)
    
    Space Complexity:
    - Best Case: O(log n)
    - Average Vase: O(log n)
    - Worst Case: O(n)
    
    """
    less = []
    equal = []
    greater = []

    if len(array) > 1:
        pivot = array[0]
        for x in array:
            if x < pivot:
                less.append(x)
            elif x == pivot:
                equal.append(x)
            elif x > pivot:
                greater.append(x)
        return quick_sort(less) + equal + quick_sort(greater) 
    else:
        return array
