from data_structures_project.base import Place, Address
from data_structures_project.utils import prompt_number, display_options, prompt_date, prompt_yes_no, quick_sort, route_search

import datetime
import csv
import os
import json


class Session:
    def __init__(self):
        
        self.places = []
        
        # Hard Code some points of intrest
        self.poi = [Place(name="Park", _type="POI", neighbours={"Train Station": 42, "Library": 87}, 
                          heuristics={'Train Station': 40, 'Library': 80, 'School': 90, 'Museum': 50, 'Cinema': 90}),
                    Place(name="Train Station", _type="POI", neighbours={"Park": 42, "Library": 94, "School": 51, "Museum": 36}, 
                          heuristics={'Park': 40, 'Library': 60, 'School': 50, 'Museum': 35, 'Cinema': 80}),
                    Place(name="Library", _type="POI", neighbours={"Park": 87, "Train Station": 94, "School": 28, "Cinema": 85}, 
                          heuristics={'Park': 80, 'Train Station': 60, 'School': 20, 'Museum': 70, 'Cinema': 70}),
                    Place(name="School", _type="POI", neighbours={"Train Station": 51, "Library": 28, "Cinema": 39}, 
                          heuristics={'Park': 90, 'Train Station': 50, 'Library': 20, 'Museum': 60, 'Cinema': 40}),
                    Place(name="Museum", _type="POI", neighbours={"Train Station": 36, "Cinema": 99}, 
                          heuristics={'Park': 50, 'Train Station': 35, 'Library': 70, 'School': 60, 'Cinema': 60}),
                    Place(name="Cinema", _type="POI", neighbours={"Library": 85, "School": 39, "Museum": 99}, 
                          heuristics={'Park': 90, 'Train Station': 80, 'Library': 70, 'School': 40, 'Museum': 60})]
        
        # Read in from the CSV
        if os.path.exists("csv/places_to_stay.csv"):
            with (open("csv/places_to_stay.csv", "r") as places_to_stay_csv, 
                  open("csv/bookings.csv", "r") as bookings_csv, 
                  open("csv/enquiries.csv", "r") as enquiries_csv,
                  open("csv/neighbours.csv", "r") as neighbours_csv,
                  open("csv/heuristics.csv") as heuristics_csv):
                csv_reader_places_to_stay = csv.reader(places_to_stay_csv)
                csv_reader_bookings = csv.reader(bookings_csv)
                csv_reader_enquiries = csv.reader(enquiries_csv)
                csv_reader_neighbours = csv.reader(neighbours_csv)
                csv_reader_heuristics = csv.reader(heuristics_csv)
                next(csv_reader_places_to_stay, None)
                next(csv_reader_bookings, None)
                next(csv_reader_enquiries, None)
                next(csv_reader_neighbours, None)
                next(csv_reader_heuristics, None)
                places_to_stay = []
                for row in csv_reader_places_to_stay:
                    address_number, address_name, address_postcode = row[2].split("-")
                    places_to_stay.append(Place(name=row[0], 
                                                     _type=row[1],
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
                            
                for row in csv_reader_neighbours:
                    for place in [*places_to_stay, *self.poi]:
                        if row[0] == place.name:
                            place.neighbours[row[1]] = int(row[2])
                            
                for row in csv_reader_heuristics:
                    for place in [*places_to_stay, *self.poi]:
                        if row[0] == place.name:
                            place.heuristics[row[1]] = int(row[2])
                
                self.places = places_to_stay
                self.update_csv()
        self.main_loop()
        
    def find_place(self, prompt="Please enter the name of the place to stay: ", include_poi=False, route=False):
        """
        Accepts a name, and checks if it is in the list
        """
        if not include_poi:
            if len(self.places) == 0:
                print("No places found.")
                return None
        found = False
        while not found:
            name = input(prompt)
            if include_poi:
                for place in [*self.places, *self.poi]:
                    if name == place:
                        if route:
                            if place.neighbours:
                                found = True
                                break # break for loop
                        else:
                            found = True
                            break # break for loop
            else:
                for place in self.places:
                    if name == place:
                        found = True
                        break # break for loop
            if not found:
                print("Name not found, please try again.")
        return place
    
    def update_csv(self):
        with open("csv/places_to_stay.csv", "w", newline="") as f:
            csvwriter = csv.writer(f)
            csvwriter.writerow(["name", "type", "address", "avalability"])
            for place in self.places:
                row = []
                for item in place:
                    row.append(item)
                csvwriter.writerow(row)
                
        with open("csv/bookings.csv", "w", newline="") as f:
            csvwriter = csv.writer(f)
            csvwriter.writerow(["name", "date", "slots_remaining"])
            for place in self.places:
                for date, amount in place.bookings.items():
                    csvwriter.writerow([place.name, date.strftime("%d-%m-%Y"), amount])
                    
        with open("csv/enquiries.csv", "w", newline="") as f:
            csvwriter = csv.writer(f)
            csvwriter.writerow(["name", "enquiry"])
            for place in self.places:
                for enquiry in place.enquiries:
                    csvwriter.writerow([place.name, enquiry])
                    
        with open("csv/neighbours.csv", "w", newline="") as f:
            csvwriter = csv.writer(f)
            csvwriter.writerow(["name", "neighbour"])
            for place in [*self.places, *self.poi]:
                if place.neighbours:
                    for neighbour, distance in place.neighbours.items():
                        csvwriter.writerow([place.name, neighbour, distance])
                    
        with open("csv/heuristics.csv", "w", newline="") as f:
            csvwriter = csv.writer(f)
            csvwriter.writerow(["starting_place", "ending_place", "distance"])
            for place in [*self.places, *self.poi]:
                if place.heuristics:
                    for ending_place, distance in place.heuristics.items():
                        csvwriter.writerow([place.name, ending_place, distance])

    def add_place(self):
        """
        Adds a place to stay, append to a CSV
        """
        name = input("Please enter the name: ")
        valid_types = ["Hotel", "Hostel", "BNB"]
        display_options(options=valid_types)
        _type = valid_types[prompt_number(prompt="Please enter the type: ", _range=(1, len(valid_types)))-1]
        address = Address()
        address.get()
        avalability = prompt_number(prompt="Please enter the avalability (number of parties per night): ")
        
        enable_routing = prompt_yes_no(prompt="Do you want to enable routing for this place to stay (Y/N)? ")
        
        if enable_routing:
            neighbours = {}
            num_neighbours = prompt_number(prompt=f"How many neighbours does {name} have? ")
            
            for i in range(1, num_neighbours+1):
                place = self.find_place(prompt=f"Please enter neighbour {i}: ", include_poi=True, route=True)
                distance = prompt_number(prompt=f"Please enter the distance to {place.name}: ")
                neighbours[place.name] = distance
                place.neighbours[name] = distance  # Add the neighbour to both the newly added place and the existing place
                            
            heuristics = {}
            for place in [*self.places, *self.poi]:
                if place.neighbours:
                    straight_distance = prompt_number(prompt=f"Please enter the straight-line distance to {place.name}: ")
                    heuristics[place.name] = straight_distance
                    place.heuristics[name] = straight_distance  # Add the heuristics to both the newly added place and the existing place
            else:
                heuristics = None
        else:
            neighbours = None
            heuristics = None
                
        
        place = Place(name=name, _type=_type, address=address, avalability=avalability, neighbours=neighbours, heuristics=heuristics)
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
                
                
    def find_route(self):
        starting_place = self.find_place(prompt="Please enter the starting location: ", include_poi=True, route=True)
        if starting_place is None:
            return
        
        ending_place = self.find_place(prompt="Please enter the starting location: ", include_poi=True, route=True)
        if ending_place is None:
            return
        
        weighted_graph = {}
        for place in [*self.places, *self.poi]:
            if place.neighbours:
                weighted_graph[place.name] = place.neighbours
                
        use_heuristics = prompt_yes_no(prompt="Use heuristics (Y/N)? ")
                
        if use_heuristics:
            heuristics = {}
            for place in [*self.places, *self.poi]:
                if place.heuristics:
                    heuristics[place.name] = place.heuristics
        else:
            heuristics = None
        
        path = route_search(weighted_graph, starting_place.name, ending_place.name, a_star_heuristics=heuristics)
        print(*path[0], sep='->')
        print(f"Distance: {path[1]}")
                
        
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
              "7.\tFind Route\n"
              "8.\tExit\n")
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
                    self.find_route()

                case 8:
                    quit()


if __name__ == "__main__":
    Session()
