"""
Defines CreateGraph class which creates a graph as an adjacency list from a 2D array.

Imports:
    numpy

Classes:
    CreateGraph
"""
import numpy as np

class CreateGraph:
    """
    A class to create a graph as an adjacency list from a 2D array (the map).

    Attributes:
        __map (np.ndarray): A 2D array representing the tilemap.
    """
    def __init__(self, map_array: np.ndarray) -> None:
        """
        Initialises the CreateGraph class with the given map.

        Args:
            map_array (np.ndarray): A 2D array representing the tilemap.
        """
        self.__map: np.ndarray = map_array

    def make_graph(self) -> dict[tuple[int, int], list[tuple[int, int]]]:
        """
        Creates a graph where each building is a node and edges exist between all pairs of nodes.

        Returns:
            dict[tuple[int, int],
                 list[tuple[int, int]]]: Dictionary representing graph.
                                         Keys are nodes, and values are lists of neighbouring nodes.
        """
        rows: int = len(self.__map)
        columns: int = len(self.__map[0])
        graph: dict[tuple[int, int], list[tuple[int, int]]] = {}
        points: list[tuple[int, int]] = []

        for i in range(rows):
            for j in range(columns):
                if self.__map[i][j] != 0:
                    points.append((i, j)) # Add coordinates to points list if tile is a building (non-zero)

        for point in points:
            graph[point] = []
            for other_point in points:
                if point != other_point: # Avoid self loops
                    graph[point].append(other_point) # Add points to graph

        return graph
