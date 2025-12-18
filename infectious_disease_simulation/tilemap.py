"""
Defines Tilemap class which creates a random tilemap with buildings.

Imports:
    random
    numpy
    pygame
    buildings: Types of buildings and their properties.
    display: Holds display properties, pygame modules, to manage display window.

Classes:
    Tilemap
"""
import random
import numpy as np
import pygame
from . import buildings
from . import display # For typing

class Tilemap:
    """
    A class to create a tilemap on which different types of buildings can be placed and displayed.

    Attributes:
        __display (display.Display): Display surface on which the tilemap will be rendered.
        __building_width (int): The width of the building to be displayed in the tilemap.
        __building_height (int): The height of the building to be displayed in the tilemap.
        __size (tuple[int, int]): Number of tiles, depending on display size and building size.
        __map (np.ndarray): A 2D array representing the tilemap grid, initialised with 0s.
        __houses (list[buildings.House]): List of House objects in the tilemap.
        __offices (list[building.Office]): List of Office objects in the tilemap.
        __buildings (list[buildings.Building]): List of the buildings in the tilemap.
        __num_houses (int): The number of houses to be placed on the tilemap.
        __num_offices (int): The number of offices to be placed on the tilemap.
        __current_houses (int): Current number of houses placed on the tilemap, initialised to 0.
        __current_offices (int): Current number of offices placed on the tilemap, initialised to 0.
    """
    def __init__(self, display_obj: display.Display,
                 num_houses: int, num_offices: int,
                 building_width: int, building_height: int) -> None:
        """
        Initialises the tilemap with the given parameters.

        Args:
            display_obj (display.Display): Display surface on which the tilemap will be rendered.
            num_houses (int): The maximum number of houses that can be placed on the tilemap.
            num_offices (int): The maximum number of offices that can be placed on the tilemap.
            building_width (int): The width of each building in the tilemap.
            building_height (int): The height of each building in the tilemap.
        """
        self.__display: display.Display = display_obj
        self.__building_width: int = building_width
        self.__building_height: int = building_height
        self.__size: tuple[int, int] = (int(self.__display.get_width() / building_width),
                                        int(self.__display.get_height() / building_height))
        self.__map: np.ndarray = np.zeros(self.__size, dtype=int) # Array of 0s of size self.__size
        self.__houses: list[buildings.House] = []
        self.__offices: list[buildings.Office] = []
        self.__buildings: list[buildings.Building] = []
        self.__num_houses: int = num_houses
        self.__num_offices: int = num_offices
        self.__current_houses: int = 0
        self.__current_offices: int = 0

    def get_num_houses(self) -> int:
        """
        Returns the number of houses to be placed on the tilemap.

        Returns:
            int: The number of houses to be placed.
        """
        return self.__num_houses

    def get_houses(self) -> list[buildings.House]:
        """
        Returns the list of houses placed on the tilemap.
        
        Returns:
            list[buildings.House]: The list of houses.
        """
        return self.__houses

    def get_offices(self) -> list[buildings.Office]:
        """
        Returns the list of offices placed on the tilemap.
        
        Returns:
            list[buildings.Office]: The list of offices.
        """
        return self.__offices

    def get_buildings(self) -> list[buildings.Building]:
        """
        Returns the list of buildings placed on the tilemap.
        
        Returns:
            list[buildings.Building]: The list of buildings.
        """
        return self.__buildings

    def get_home_from_location(self, location: tuple[int, int]) -> buildings.House:
        """
        Returns the house object from a coordinate location.

        Returns:
            buildings.House: The House object with the required location.
        """
        for house in self.__houses:
            if house.get_location() == location:
                return house
        return None

    def get_office_from_location(self, location: tuple[int, int]) -> buildings.Office:
        """
        Returns the office object from a coordinate location.

        Returns:
            buildings.Office: The Office object with the required location.
        """
        for office in self.__offices:
            if office.get_location() == location:
                return office
        return None

    def get_map(self) -> np.ndarray:
        """
        Returns the state of the tilemap as an array.
        
        Returns:
            np.ndarray: A 2D array representing the tilemap.
        """
        return self.__map

    def get_building_width(self) -> int:
        """
        Returns the width of a building in the tilemap (pixels).

        Returns:
            int: The building width
        """
        return self.__building_width

    def get_building_height(self) -> int:
        """
        Returns the height of a building in the tilemap (pixels).

        Returns:
            int: The building height
        """
        return self.__building_height

    def __place_building(self, building_type: str, empty_locations: list[tuple[int, int]]) -> None:
        """
        Places a building of the specified type on the tilemap at a random, empty location.
        If location not empty, random values generated until an empty location is found.

        Args:
            building_type (str): The type of building to place.
            empty_locations (list[tuple[int, int]]): List of available empty locations on the tilemap.
        """
        if not empty_locations:
            return  # No empty locations available
        
        x, y = random.choice(empty_locations) # random empty location

        # NOTE
        # [x, y] flipped due to differences in coordinate systems in Python/ NumPy and Pygame
        # Python/ NumPy: first index = row (y), second index = column (x)
        # Pygame: first index = column (x), second index = row (y)
        if building_type == "house" and self.__current_houses < self.__num_houses:
            building = buildings.House((x, y))
            self.__houses.append(building) # Add to list of houses
            self.__map[y, x] = 1
            self.__current_houses += 1
        elif building_type == "office" and self.__current_offices < self. __num_offices:
            building = buildings.Office((x, y))
            self.__offices.append(building) # Add to list of offices
            self.__map[y, x] = 2
            self.__current_offices += 1

        self.__buildings.append(building) # Add to list of buildings
        empty_locations.remove((x, y))


    def render(self, pause: bool) -> None:
        """
        Renders all buildings on the display.
        Draws each building as a rectangle on the display surface using its location and dimensions.

        Args:
            pause (bool): True if display process to be shown, False if not.
        """
        # Get empty locations on the tilemap
        empty_locations: list[tuple[int, int]] = [(x, y)
                                                  for x in range(self.__size[0])
                                                  for y in range(self.__size[1])
                                                  if self.__map[y, x] == 0]

        # Loop through number of houses, offices and place on tilemap
        for building, max_count in [("house", self.__num_houses),
                                    ("office", self.__num_offices),]:
            for _ in range(max_count):
                self.__place_building(building, empty_locations)

        for building in self.__buildings:
            x, y = building.get_location()
            pygame.draw.rect(self.__display.get_screen(), # Display surface
                             building.get_colour(), # Colour
                             (x * self.__building_width, # Top left coord
                              y * self.__building_height, # Top right coord
                              self.__building_width, # Bottom left coord
                              self.__building_height)) # Bottom right coord
            if pause:
                self.__display.update()
                pygame.time.wait(2) # Wait to show drawing process
