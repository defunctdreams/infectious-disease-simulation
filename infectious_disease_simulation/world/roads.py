"""
Defines Roads class which handles and draws roads on the map.

Imports:
    pygame
    numpy
    display: Holds display properties, pygame modules, to manage display window
    mst: Creates Minimum Spanning Tree using Kruskal on graph of the map

Classes:
    Roads
"""
import pygame
import numpy as np
from ..display import Display # For typing
from .graph import mst

class Roads:
    """
    A class to manage and draw roads on the tilemap.

    Attributes:
        __display (display.Display): The display surface on which the roads will be drawn.
        __map (np.ndarray): A 2D array representing the tilemap.
        __building_width (int): The width of each building in the tilemap.
        __building_height (int): The height of each building in the tilemap.
        __additional_roads (bool): True if additional roads to be included, False if not.
        __mst_dict (dict[tuple[int, int], list[tuple[tuple[int, int], int]]]): Dictionary containing the roads.
    """
    def __init__(self,
                 display_obj: Display,
                 map_array: np.ndarray,
                 building_width: int, building_height: int,
                 additional_roads: bool) -> None:
        """
        Initialises the Roads class with the given parameters.

        Args:
            display_obj (display.Display): The display surface on which the roads will be drawn.
            map_array (np.ndarray): A 2D array representing the tilemap.
            building_width (int): The width of each building in the tilemap.
            building_height (int): The height of each building in the tilemap.
            additional_roads (bool): True if additional roads to be included.
        """
        self.__display: Display = display_obj
        self.__map: np.ndarray = map_array
        self.__building_width: int = building_width
        self.__building_height: int = building_height
        self.__additional_roads: bool = additional_roads
        self.__mst_dict: dict[tuple[int, int],
                              list[tuple[tuple[int, int], int]]] = mst.MST(self.__map).get_mst(self.__additional_roads)

    def get_roads(self) -> dict[tuple[int, int], list[tuple[tuple[int, int], int]]]:
        """
        Returns the roads generated.

        Returns:
            dict[tuple[int, int], list[tuple[tuple[int, int], int]]]: Dictionary of roads generated.
        """
        return self.__mst_dict

    def draw_roads(self, pause: bool) -> None:
        """
        Draws roads on the tilemap based on the minimum spanning tree (MST) of the map.

        Args:
            pause (bool): If True, briefly pauses to show the drawing process.
        """
        for point, neighbours in self.__mst_dict.items():
            x1, y1 = point # Current point
            for neighbour, _ in neighbours:
                x2, y2 = neighbour # Neighbouring point
                pygame.draw.line(self.__display.get_screen(), # Screen surface
                                 (125, 125, 125), # Colour
                                 (x1 * self.__building_width + self.__building_width // 2, # Start
                                  y1 * self.__building_height + self.__building_height // 2),
                                 (x2 * self.__building_width + self.__building_width // 2, # End
                                  y2 * self.__building_height + self.__building_height // 2),
                                 5) # Line thickness

                if pause:
                    self.__display.update()
                    pygame.time.wait(2) # Wait ot show drawing process
