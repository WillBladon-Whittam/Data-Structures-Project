from base import PlaceToStay, Address, Type

from utils import prompt_number, display_options, prompt_date

import datetime


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
        avalability = prompt_number(prompt="Please enter the avalability (number of parties per night): ")
        self.places.append(PlaceToStay(name=name, _type=type_, address=address, avalability=avalability))
        
    def search_place(self):
        """
        Searchs for a place to stay. Searchs based on name, address and type
        """
        search_value = input("SEARCH: ")
        
        matched_places = []
        for place in self.places:
            if search_value in place:
                matched_places.append(place)
        
        matched_places.sort()
        display_options(options=matched_places)
        
    def display_all_places(self):
        """
        Display all places to stay.
        """
        self.places.sort()
        display_options(options=self.places)
        
    def make_booking(self):
        """
        Make a booking for a specifc date
        """
        found = False
        while not found:
            name = input("Please enter the name of the booking: ")
            for place in self.places:
                if name == place:
                    found = True
            if not found:
                print("Name not found, please try again.")
        
        date = prompt_date(prompt="Please enter the date of the booking (DD-MM-YYYY): ", _range=(datetime.date.today(), None))
        number = prompt_number(prompt="Please enter the number of slots to book: ")
        
        place.book(date=date, number=number)

    def main_menu(self) -> int:
        """
        Displays the main menu, returning the navigation integer
        """
        print("\nPlaces to Stay Main Menu\n"
              "----------------------------------------------------\n"
              "1.\tAdd a place to stay\n" # Add save to file, book, routing and enquire to this
              "2.\tSearch for a place to stay\n"
              "3.\tShow all places to stay\n"
              "4.\tMake a Booking\n"
              "5.\tAnswer Enquires\n"
              "6.\tExit\n")
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
                    self.display_all_places()

                case 4:
                    self.make_booking()
                
                case 5:
                    raise NotImplemented

                case 6:
                    quit()


if __name__ == "__main__":
    Session()
