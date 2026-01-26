"""
Defines AdditionalConnections class which manages additional connections from a MST.

Imports:
    math

Classes:
    AdditionalConnections
"""

import math

class AdditionalConnections:
    """
    A class to manage additional connections in a Minimum Spanning Tree (MST).

    Attributes:
        __mst (dict[tuple[int, int], list[tuple[tuple[int, int], int]]]): The MST.
    """
    def __init__(self, mst: dict[tuple[int, int], list[tuple[tuple[int, int], int]]]) -> None:
        """
        Initialises the AdditionalConnections class with the given MST.

        Args:
            mst (dict[tuple[int, int], list[tuple[tuple[int, int], int]]]): The MST.
        """
        self.__mst: dict[tuple[int, int], list[tuple[tuple[int, int], int]]] = mst

    def add_connections(self, min_distance: int = 3) -> dict[tuple[int, int],
                                                             list[tuple[tuple[int, int], int]]]:
        """
        Adds additional connections to the MST based on a minimum distance.

        Args:
            min_distance (int): The minimum distance between nodes to add connection. Defaults to 3.

        Returns:
            dict[tuple[int, int],
            list[tuple[tuple[int, int], int]]]: The updated MST with additional connections.
        """
        single_connection_nodes: list[tuple[int, int]] = []

        # Find all nodes with a single connection in the MST
        for node in self.__mst:
            if len(self.__mst[node]) == 1:
                single_connection_nodes.append(node)

        # Add additional connections based on the minimum distance
        for node in single_connection_nodes:
            nearest_node: tuple[int, int] = None
            for other_node in single_connection_nodes:
                if node != other_node: # Check for same node
                    distance: int = self.__calculate_weight(node, other_node)

                    if (distance > min_distance) and not self.__crosses_existing_edges(node, other_node):
                        nearest_node = other_node

            # If a nearest node is found, add the connection
            if nearest_node:
                self.__mst[node].append((nearest_node, distance))
                self.__mst[nearest_node].append((node, distance))

        return self.__mst

    def __crosses_existing_edges(self, node1: tuple[int, int], node2: tuple[int, int]) -> bool:
        """
        Checks if a new edge between two nodes crosses any existing edges in the MST.

        Args:
            node1 (tuple[int, int]): The first node.
            node2 (tuple[int, int]): The second node.

        Returns:
            bool: True if the new edge crosses any existing edges, False otherwise.
        """
        for node in self.__mst:
            for neighbour, _ in self.__mst[node]:
                if self.__do_edges_cross(node, neighbour, node1, node2):
                    return True
        return False

    def __do_edges_cross(self, a1: tuple[int, int], a2: tuple[int, int],
                         b1: tuple[int, int], b2: tuple[int, int]) -> bool:
        """
        Checks if two edges (a1, a2) and (b1, b2) cross each other.

        NOTE
        Happens only when the points a1 and a2 are on opposite sides of the line segment (b1, b2),
        and the points b1 and b2 are on opposite sides of the line segment (a1, a2).
        Check if a1, b1, b2 are anticlockwise and a2, b1, b2 are not anticlockwise, and vice versa.
        If both conditions are true, the line segments cross.

        Args:
            a1 (tuple[int, int]): The first endpoint of the first edge.
            a2 (tuple[int, int]): The second endpoint of the first edge.
            b1 (tuple[int, int]): The first endpoint of the second edge.
            b2 (tuple[int, int]): The second endpoint of the second edge.

        Returns:
            bool: True if the edges cross each other, False otherwise.
        """
        return self.__acw(a1, b1, b2) != self.__acw(a2, b1, b2) and self.__acw(a1, a2, b1) != self.__acw(a1, a2, b2)

    def __acw(self, point1: tuple[int, int], point2: tuple[int, int], point3: tuple[int, int]) -> bool:
        """
        Checks if three points are listed in a anticlockwise order.

        Args:
            point1 (tuple[int, int]): The first point.
            point2 (tuple[int, int]): The second point.
            point3 (tuple[int, int]): The third point.

        Returns:
            bool: True if the points are in anticlockwise order, False otherwise.
        """
        return (point3[1] - point1[1]) * (point2[0] - point1[0]) > (point2[1] - point1[1]) * (point3[0] - point1[0])

    def __calculate_weight(self, node1: tuple[int, int], node2: tuple[int, int]) -> int:
        """
        Calculates the weight (distance) between two nodes.

        Args:
            node1 (tuple[int, int]): The first node.
            node2 (tuple[int, int]): The second node.

        Returns:
            int: The distance between the two nodes.
        """
        weight: int = int(math.sqrt((node1[0] - node2[0]) ** 2 + (node1[1] - node2[1]) ** 2))
        return weight
