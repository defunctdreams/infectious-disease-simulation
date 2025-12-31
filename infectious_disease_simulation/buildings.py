""" 
Defines classes for different types of buildings and their properties.

Imports:
    abc: For creating abstract base classes.
    person: Class managing and holding a simulated person's properties and person-specific methods.

Classes:
    Building
    House
    Office
"""
from abc import ABC, abstractmethod
from . import person # For typing

class Building(ABC):
    """
    A class representing a building.

    Attributes:
        __location (tuple[int, int]): The location of the building.
        __colour (tuple[int, int, int]): The colour of the building.
        __occupants (list[person.Person]): The list of occupants in the building.
    """
    def __init__(self, location: tuple[int, int], colour: tuple[int, int, int]) -> None:
        """
        Initialises the Building class with the given parameters.

        Args:
            location (tuple[int, int]): The location of the building.
            colour (tuple[int, int, int]): The colour of the building.
        """
        self.__location: tuple[int, int] = location
        self.__colour: tuple[int, int, int] = colour
        self.__occupants: list[person.Person] = []

    def get_location(self) -> tuple[int, int]:
        """
        Gets the location of the building.

        Returns:
            tuple[int, int]: The location of the building.
        """
        return self.__location

    def get_occupants(self) -> list[person.Person]:
        """
        Gets the occupants of the building.

        Returns:
            list[person.Person]: The list of occupants in the building.
        """
        return self.__occupants

    def add_occupant(self, occupant: person.Person) -> None:
        """
        Adds an occupant to the building.

        Args:
            occupant (person.Person): The person to be added as an occupant.
        """
        self.__occupants.append(occupant)

    def get_colour(self) -> tuple[int, int, int]:
        """
        Gets the colour of the building.

        Returns:
            tuple[int, int, int]: The colour of the building.
        """
        return self.__colour
    
    @abstractmethod
    def get_tile_value(self) -> int:
        """
        Gets the tile value of the building based on its type.
        
        Returns:
            int: The tile value of the building.
        """
        pass

class House(Building):
    """
    A class representing a house, inherits from Building.
    """
    def __init__(self, location: tuple[int, int]) -> None:
        """
        Initialises the House class with the given location.

        Args:
            location (tuple[int, int]): The location of the house.
        """
        super().__init__(location, (100, 200, 100))

    def get_tile_value(self) -> int:
        return 1

class Office(Building):
    """
    A class representing an office, inherits from Building.
    """
    def __init__(self, location: tuple[int, int]) -> None:
        """
        Initialises the Office class with the given location.

        Args:
            location (tuple[int, int]): The location of the office.
        """
        super().__init__(location, (100, 100, 200))
    
    def get_tile_value(self) -> int:
        return 2
