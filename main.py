from base import PlaceToStay, Address, Type
from utils import prompt_number, display_options, prompt_date, prompt_yes_no, quick_sort

import datetime
import csv
import os
import json


class Session:
    def __init__(self):
        self.places = []
        
        # Read in from the CSV
        if os.path.exists("places_to_stay.csv"):
            with open("places_to_stay.csv", "r") as places_to_stay_csv, open("bookings.csv", "r") as bookings_csv, open("enquiries.csv", "r") as enquiries_csv:
                csv_reader_places_to_stay = csv.reader(places_to_stay_csv)
                csv_reader_bookings = csv.reader(bookings_csv)
                csv_reader_enquiries = csv.reader(enquiries_csv)
                next(csv_reader_places_to_stay, None)
                next(csv_reader_bookings, None)
                next(csv_reader_enquiries, None)
                places_to_stay = []
                for row in csv_reader_places_to_stay:
                    address_number, address_name, address_postcode = row[2].split("-")
                    places_to_stay.append(PlaceToStay(name=row[0], 
                                                     _type=Type(_type=row[1]),
                                                     address=Address(number=address_number.strip(), roadname=address_name.strip(), postcode=address_postcode.strip()),
                                                     avalability=int(row[3])))
        
                for row in csv_reader_bookings:
                    for place in places_to_stay:
                        if row[0] == place.name:
                            place.bookings[datetime.datetime.strptime(row[1], "%d-%m-%Y")] = row[2]
                            
                for row in csv_reader_enquiries:
                    for place in places_to_stay:
                        if row[0] == place.name:
                            place.enquiries.append(row[1])
                
                self.places = places_to_stay
        self.main_loop()
        
    def find_place(self):
        """
        Accepts a name, and checks if it is in the list
        """
        if len(self.places) == 0:
            print("No places found.")
            return None
        found = False
        while not found:
            name = input("Please enter the name of the place to stay: ")
            for place in self.places:
                if name == place:
                    found = True
                    break # break for loop
            if not found:
                print("Name not found, please try again.")
        return place
    
    def update_csv(self):
        with open("places_to_stay.csv", "w", newline="") as f:
            csvwriter = csv.writer(f)
            csvwriter.writerow(["name", "type", "address", "avalability"])
            for place in self.places:
                row = []
                for item in place:
                    row.append(item)
                csvwriter.writerow(row)
                
        with open("bookings.csv", "w", newline="") as f:
            csvwriter = csv.writer(f)
            csvwriter.writerow(["name", "date", "slots_remaining"])
            for place in self.places:
                for date, amount in place.bookings.items():
                    csvwriter.writerow([place.name, date.strftime("%d-%m-%Y"), amount])
                    
        with open("enquiries.csv", "w", newline="") as f:
            csvwriter = csv.writer(f)
            csvwriter.writerow(["name", "enquiry"])
            for place in self.places:
                for enquiry in place.enquiries:
                    csvwriter.writerow([place.name, enquiry])

    def add_place(self):
        """
        Adds a place to stay, append to a CSV
        """
        name = input("Please enter the name: ")
        type_ = Type()
        type_.get()
        address = Address()
        address.get()
        avalability = prompt_number(prompt="Please enter the avalability (number of parties per night): ")
        
        place = PlaceToStay(name=name, _type=type_, address=address, avalability=avalability)
        self.places.append(place)
        self.update_csv()
        
    def search_place(self):
        """
        Searchs for a place to stay. Searchs based on name, address and type
        """
        search_value = input("SEARCH: ")
        
        matched_places = []
        for place in self.places:
            if search_value in place:
                matched_places.append(place)
        
        matched_places = quick_sort(matched_places)
        display_options(options=matched_places, empty_prompt="No places found!")
        
    def display_all_places(self):
        """
        Display all places to stay.
        """
        self.places = quick_sort(self.places)
        display_options(options=self.places, empty_prompt="No places found!")
        
    def make_booking(self):
        """
        Make a booking for a specifc date
        """
        place = self.find_place()
        if place is None:
            return
        date = prompt_date(prompt="Please enter the date of the booking (DD-MM-YYYY): ", _range=(datetime.date.today(), None))
        number = prompt_number(prompt="Please enter the number of slots to book: ")

        place.book(date=date, number=number)
        self.update_csv()
            
        
    def make_enquiry(self):
        place = self.find_place()
        if place is None:
            return

        enquiry = input(f"Please enter your enquiry for the staff of {place.name}: ")
        place.enquiries.append(enquiry)
        self.update_csv()
        
        print("Thank you. Your enquiry has been placed")
        
    def answer_enquiry(self):
        place = self.find_place()
        if place is None:
            return
        
        if len(place.enquiries) == 0:
            print("No Enquiries found")
            return
                
        print(f"{len(place.enquiries)} Enquirys Found")
        
        counter = 0
        while counter < len(place.enquiries):
            print(f"Enquiry {counter+1}: {place.enquiries[counter]}")
            answer = prompt_yes_no("Do you want to answer this enquiry (Y/N)? ")
            if answer:
                place.enquiries.pop(counter)
                self.update_csv()
                print("The enquiry has been answered!")
            else:
                print("The enquiry has not been answered!")
                counter += 1
                
        
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
              "5.\tMake an Enquiry\n"
              "6.\tAnswer Enquiries\n"
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
                    self.display_all_places()

                case 4:
                    self.make_booking()
                
                case 5:
                    self.make_enquiry()
                    
                case 6:
                    self.answer_enquiry()

                case 7:
                    quit()


if __name__ == "__main__":
    Session()
