from typing import Tuple, Union


class Session:
    def __init__(self):
        self.main_loop()

    @staticmethod
    def prompt_number(prompt: str, _range: Tuple[int, Union[int, None]] = None,
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

    def main_menu(self) -> int:
        """
        Displays the main menu, returning the navigation integer
        """
        print("Hotels Main Menu\n"
              "----------------------------------------------------\n"
              "1.\tAdd a place to stay\n"
              "2.\tSearch for a place to stay\n"  # Add save to file, book, routing and enquire to this
              "3.\tShow all places to stay\n"
              "4.\tSearch for a type of place to stay\n"
              "5.\tAnswer Enquires\n"
              "7.\tExit\n")
        return self.prompt_number("Select an option: ", _range=(1, 7))

    def main_loop(self) -> None:
        """
        The main loop of the session
        """
        while True:
            # NOTE: match/case statements are python 3.10+
            match self.main_menu():

                case 1:
                    raise NotImplemented

                case 2:
                    raise NotImplemented

                case 3:
                    raise NotImplemented

                case 4:
                    raise NotImplemented

                case 5:
                    raise NotImplemented

                case 6:
                    raise NotImplemented

                case 7:
                    raise NotImplemented

if __name__ == "__main__":
    Session()