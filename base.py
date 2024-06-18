from enum import Enum
import abc
from abc import ABC, abstractmethod
from typing import Literal
from utils import prompt_number, display_options


class Base(ABC):

    @abstractmethod
    def get(self):
        ...
    
    
class Address(Base):
    """
    Object to hold the address infomation of a place to stay
    """
    def __init__(self) -> None:
        self.number = None
        self.roadname = None
        self.postcode = None
        
        self.get()
        
    def __str__(self) -> str:
        return f"{self.number} {self.roadname}, {self.postcode}"
    
    def __contains__(self, search_value):
        if search_value in str(self.number):
            return True
        elif search_value in self.roadname:
            return True
        elif search_value in self.postcode:
            return True
    
    def get(self):
        self.number = prompt_number(prompt="Please enter your house number: ")
        self.roadname = input("Please enter your road name: ")
        self.postcode = input("Please enter your postcode: ").strip()


# Just use an enum maybe?
class Type(Base):
    """
    Object to hold the type of a place to stay
    """
    def __init__(self) -> None:
        self.type = None
        self.valid_types = ["Hotel", "Hostel", "BNB"]
        
        self.get()
        
    def __str__(self) -> str:
        return f"{self.type}"
    
    def __contains__(self, search_value):
        if search_value in self.type:
            return True
    
    def get(self):
        display_options(options=self.valid_types)
        self.type = self.valid_types[prompt_number(prompt="Please enter the type: ", _range=(1, len(self.valid_types)))-1]


class PlaceToStay:
    """
    Object to hold infomation about a place to stay
    """
    def __init__(self, name: str, _type: Type, address: Address, avalability: int):
        self.name = name
        self.type = _type
        self.address = address
        
        self.avalability = avalability
        
        # Stores the date as the key and the number of avaliable rooms
        self.bookings = {}
        
    def __str__(self) -> str:
        return f"Name: {self.name} \nType: {self.type} \nAddress: {self.address}"
    
    def __contains__(self, search_value):
        if search_value in self.name:
            return True
        elif search_value in self.type:
            return True
        elif search_value in self.address:
            return True
        
    def __gt__(self, other):
        return self.name > other
        
    def __lt__(self, other):
        return self.name < other
    
    def __eq__(self, other):
        return self.name == other
    
    def book(self, date, number):
        """
        Books slots for the room, taking the date and number of slots as arguments
        """
        if date not in self.bookings.keys():
            self.bookings[date] = self.avalability
            
        if self.bookings[date] < number:
            print(f"Only {self.bookings[date]} slots left! {number} is too many to book!")
        else:
            self.bookings[date] = self.bookings[date] - number
            print(f"Successfully booked {number} slots on {date}!")
        
    
    
        
        