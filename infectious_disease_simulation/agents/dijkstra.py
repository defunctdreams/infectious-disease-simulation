"""
Implements Dijkstra's algorithm for finding the shortest path in a graph.

Classes:
    Dijkstra
    PriorityQueue
"""

class Dijkstra:
    """
    A class to compute the shortest path using Dijkstra's algorithm.

    Attributes:
        __graph (dict[tuple[int, int], list[tuple[tuple[int, int], int]]]): The graph representation.
        __queue (PriorityQueue): The priority queue for managing nodes.
        __distances (dict[tuple[int, int], float]): The distances from the start node to other nodes.
        __previous (dict[tuple[int, int], tuple[int, int]]): The previous node in the path.
    """
    def __init__(self, graph: dict[tuple[int, int], list[tuple[tuple[int, int], int]]]) -> None:
        """
        Initialises the Dijkstra class with the given graph.

        Args:
            graph (dict[tuple[int, int], list[tuple[tuple[int, int], int]]]): The graph representation.
        """
        self.__graph: dict[tuple[int, int], list[tuple[tuple[int, int], int]]] = graph
        self.__queue: PriorityQueue = PriorityQueue()
        self.__distances: dict[tuple[int, int], float] = {}
        self.__previous: dict[tuple[int, int], tuple[int, int]] = {}

    def compute(self, start: tuple[int, int], end: tuple[int, int]) -> tuple[list[tuple[int, int]], float]:
        """
        Computes the shortest path from start to end using Dijkstra's algorithm.

        Args:
            start (tuple[int, int]): The starting node.
            end (tuple[int, int]): The ending node.

        Returns:
            tuple[list[tuple[int, int]], float]: A tuple containing the path and the total weight.
        """
        # Initialize distances for all nodes as infinity
        for node in self.__graph:
            self.__distances[node] = float('inf')

        self.__distances[start] = 0 # Start node distance is zero
        self.__queue.insert_item(start, 0)
        self.__previous = {start: None} # Initialise to None

        # Perform dijkstra's algorithm
        while not self.__queue.is_empty():
            current_node: tuple[int, int] = self.__queue.pop_item()
            if current_node in self.__graph:
                for neighbour, weight in self.__graph[current_node]:
                    distance = self.__distances[current_node] + weight
                    if distance < self.__distances[neighbour]:
                        self.__distances[neighbour] = distance
                        self.__previous[neighbour] = current_node
                        self.__queue.insert_item(neighbour, distance)

        path: list[tuple[int, int]] = []
        total_weight: float = float('inf')

        # Trace steps to build path
        if end in self.__distances and self.__distances[end] != float('inf'):
            total_weight = self.__distances[end]
            node: tuple[int, int] = end
            while node is not None:
                path.insert(0, node)
                node = self.__previous[node]

        return path, total_weight

class PriorityQueue:
    """
    A class for managing a priority queue.

    Attributes:
        __elements (list[tuple[int, tuple[int, int]]]): The list of elements in the queue.
    """
    def __init__(self) -> None:
        """
        Initialises the PriorityQueue class.
        """
        self.__elements: list[tuple[int, tuple[int, int]]] = []

    def is_empty(self) -> bool:
        """
        Checks if the priority queue is empty.

        Returns:
            bool: True if the queue is empty, False otherwise.
        """
        if len(self.__elements) == 0:
            return True
        return False

    def insert_item(self, item: tuple[int, int], priority: int) -> None:
        """
        Inserts an item into the priority queue with the given priority and adjust its position accordingly.

        Args:
            item (tuple[int, int]): The item to be inserted.
            priority (int): The priority of the item.
        """
        self.__elements.append((priority, item))
        self.__bubble_up(len(self.__elements) - 1)

    def pop_item(self) -> tuple[int, int]:
        """
        Pops the item with the highest priority from the queue.

        Returns:
            tuple[int, int]: The item with the highest priority.

        Raises:
            IndexError: If the priority queue is empty.
        """
        if self.is_empty():
            raise IndexError("Pop from empty priority queue")

        if len(self.__elements) == 1:
            return self.__elements.pop()[1]

        # Move the last element to the root
        item = self.__elements[0]
        self.__elements[0] = self.__elements.pop()
        self.__bubble_down(0)  # Maintain heap property
        return item[1]

    def __bubble_up(self, index: int) -> None:
        """
        Bubbles up the element at the given index to maintain the heap property.

        Args:
            index (int): The index of the element to bubble up.
        """
        parent_index: int = (index - 1) // 2

        # Check if swap necessary
        if index > 0 and self.__elements[index][0] < self.__elements[parent_index][0]:
            self.__swap(index, parent_index)
            self.__bubble_up(parent_index) # Recursively bubble up parent when necessary

    def __bubble_down(self, index: int) -> None:
        """
        Bubbles down the element at the given index to maintain the heap property.

        Args:
            index (int): The index of the element to bubble down.
        """
        child_index: int = 2 * index + 1 # Index of left child

        if child_index < len(self.__elements): # Left child exists

            right_child_index = child_index + 1 # Index of right child

            # Right child exists and is less than left child
            if (right_child_index < len(self.__elements) and
                self.__elements[right_child_index][0] < self.__elements[child_index][0]):
                child_index = right_child_index # Use right child (smallest)

            if self.__elements[child_index][0] < self.__elements[index][0]:
                self.__swap(index, child_index) # Swap smallest child
                self.__bubble_down(child_index) # Recursively call until not needed

    def __swap(self, i: int, j: int) -> None:
        """
        Swaps the elements at the given indices.

        Args:
            i (int): The index of the first element.
            j (int): The index of the second element.
        """
        self.__elements[i], self.__elements[j] = self.__elements[j], self.__elements[i]
