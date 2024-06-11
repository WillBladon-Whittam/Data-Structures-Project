from base import PlaceToStay, Address, Type

from utils import prompt_number, display_options


class Session:
    def __init__(self):
        self.places = []

        self.main_loop()

    def add_place(self):
        """
        Adds a place to stay
        """
        name = input("Please enter the name: ")
        type_ = Type()
        address = Address()
        self.places.append(PlaceToStay(name=name, _type=type_, address=address))
        
    def search_place(self):
        """
        Searchs for a place to stay. Searchs based on name, address and type
        """
        search_value = input("SEARCH: ")
        
        matched_places = []
        for place in self.places:
            if search_value in place:
                matched_places.append(place)
                
        display_options(options=matched_places)

    def main_menu(self) -> int:
        """
        Displays the main menu, returning the navigation integer
        """
        print("Places to Stay Main Menu\n"
              "----------------------------------------------------\n"
              "1.\tAdd a place to stay\n" # Add save to file, book, routing and enquire to this
              "2.\tSearch for a place to stay\n"
              "3.\tShow all places to stay\n"
              "4.\tSearch for a type of place to stay\n"
              "5.\tAnswer Enquires\n"
              "7.\tExit\n")
        return prompt_number("Select an option: ", _range=(1, 7))

    def main_loop(self) -> None:
        """
        The main loop of the session
        """
        while True:
            # NOTE: match/case statements are python 3.10+
            match self.main_menu():

                case 1:  # Add a place to stay
                    self.add_place()

                case 2:
                    self.search_place()

                case 3:
                    raise NotImplemented

                case 4:
                    raise NotImplemented

                case 5:
                    raise NotImplemented

                case 6:
                    raise NotImplemented

                case 7:
                    quit()


if __name__ == "__main__":
    Session()
