"""
Defines the Population class to manage the collection of people in the simulation.

Imports:
    math
    initialise_people: Class which handles the initialisation of each person.
    display: Manages display settings and updates.
    create_map: Creates and manages the simulation map.
    tilemap: Creates the tilemap of buildings.
    disease: Simulates disease probabilities.
    person: Manages a simulated person's properties and specific methods.

Classes:
    Population
"""
import math
from . import initialise_people
from . import display # For typing
from . import create_map # For typing
from . import tilemap # For typing
from . import disease # For typing
from . import person # For typing

class Population:
    """
    A class to manage the population in the simulation.

    Attributes:
        __display (display.Display): The display object for the simulation.
        __map (create_map.CreateMap): The map object for the simulation.
        __tilemap (tilemap.Tilemap): The tilemap object for the map.
        __num_in_house (int): The number of people per house.
        __disease (disease.Disease): The disease object for the simulation.
        __seconds_per_hour (int): The number of seconds per simulation hour.
        __fps (int): The frames per second for the simulation.
        __people (list[person.Person]): The list of people in the simulation.
        __route_intersections (dict[int, list[person.Person]]): The dictionary of route intersections for each person.
    """
    def __init__(self, num_in_house: int,
                 display_obj: display.Display,
                 map_obj: create_map.CreateMap,
                 disease_obj: disease.Disease,
                 seconds_per_hour: int, fps: int) -> None:
        """
        Initialises the Population class with the given parameters.

        Args:
            num_in_house (int): The number of people per house.
            display_obj (Display): The display object for the simulation.
            map_obj (Map): The map object for the simulation.
            disease_obj (Disease): The disease object for the simulation.
            seconds_per_hour (int): The number of seconds per simulation hour.
            fps (int): The frames per second for the simulation.
        """
        self.__display: display.Display = display_obj
        self.__map: create_map.CreateMap = map_obj
        self.__tilemap: tilemap.Tilemap = self.__map.get_tilemap()
        self.__num_in_house: int = num_in_house
        self.__disease: disease.Disease = disease_obj
        self.__seconds_per_hour: int = seconds_per_hour
        self.__fps: int = fps
        self.__people: initialise_people.InitialisePeople = initialise_people.InitialisePeople(self.__num_in_house,
                                                                                               self.__display,
                                                                                               self.__map,
                                                                                               self.__disease,
                                                                                               self.__seconds_per_hour,
                                                                                               self.__fps).get_people()
        self.__route_intersections: dict[int, list[person.Person]] = self.__find_route_intersections()

    def draw_people(self) -> None:
        """
        Draws all people in the simulation on the display.
        """
        for individual in self.__people:
            individual.draw_person()

    def get_people(self) -> list[person.Person]:
        """
        Gets the list of people in the simulation.

        Returns:
            list[Person]: The list of people in the simulation.
        """
        return self.__people

    def move_to_offices(self) -> None:
        """
        Starts the movement of all people to their offices.
        """
        for individual in self.__people:
            individual.start_move_to_office()

    def move_to_homes(self) -> None:
        """
        Starts the movement of all people to their homes.
        """
        for individual in self.__people:
            individual.start_move_to_home()

    def update_positions(self) -> None:
        """
        Updates the positions of all people in the simulation and checks for interactions.
        """
        for individual in self.__people:
            individual.update_position()
            self.__check_interactions(individual)

    def update_infection_status(self) -> None:
        """
        Updates the infection status of all people in the simulation.
        """
        self.__check_building_interactions()
        for individual in self.__people:
            individual.update_infection_status()

    def has_active_infections(self) -> bool:
        """
        Checks if there are any active infections (exposed or infected) in the population.

        Returns:
            bool: True if there are active infections, False otherwise.
        """
        for individual in self.__people:
            if individual.get_status() in ["E", "I"]:
                return True
        return False

    def get_status_counts(self) -> dict[str, int]:
        """
        Gets the counts of each infection status in the population.

        Returns:
            dict[str, int]: A dictionary with the counts of each infection status.
        """
        counts: dict[str, int] = {'S': 0, 'E': 0, 'I': 0, 'R': 0, 'D': 0}
        for individual in self.__people:
            status = individual.get_status()
            counts[status] += 1
        return counts

    def __find_route_intersections(self) -> dict[int, list[person.Person]]:
        """
        Finds and returns the route intersections for each person.
        Optimisation for checking infections of the population.

        Returns:
            dict[int, list[person.Person]]: The dictionary of route intersections for each person.
        """
        """
        intersections: dict[int, list[person.Person]] = {}

        for i, individual in enumerate(self.__people):
            person_id: int = individual.get_person_id()
            person_route: set[tuple[int, int]] = set(individual.get_home_to_office_route())
            intersections[person_id] = [] # Initialise empty list of people with intersections
            for j, other_person in enumerate(self.__people):
                if i != j: # Different person
                    other_person_route: set[tuple[int, int]] = set(other_person.get_home_to_office_route())
                    if person_route.intersection(other_person_route): # Use intersection operations on sets
                        intersections[person_id].append(other_person) # Add other person to list of intersections

        return intersections
        """
        intersections: dict[int, list[person.Person]] = {}

        # Precompute route sets for each person and build tile -> people buckets
        tile_buckets: dict[tuple[int, int], list[person.Person]] = {}
        person_route_sets: dict[int, set[tuple[int, int]]] = {}

        for individual in self.__people:
            pid: int = individual.get_person_id()
            # Compute the route once and turn into a set of tiles (removes duplicate tiles)
            route_tiles: set[tuple[int, int]] = set(individual.get_home_to_office_route())
            person_route_sets[pid] = route_tiles

            # Add this person to each tile's bucket
            for tile in route_tiles:
                if tile not in tile_buckets:
                    tile_buckets[tile] = []
                tile_buckets[tile].append(individual)

        # For each person, aggregate other people who share any tile
        for individual in self.__people:
            pid: int = individual.get_person_id()
            intersections[pid] = []
            route_tiles = person_route_sets.get(pid, set())

            # Use a set to avoid duplicates when multiple tiles are shared with the same person
            others_set: set[person.Person] = set()
            for tile in route_tiles:
                for other in tile_buckets.get(tile, []):
                    if other is not individual:
                        others_set.add(other)

            # Convert to list of person.Person objects for more efficient access downstream
            intersections[pid] = list(others_set)

        return intersections

    def __check_interactions(self, individual: person.Person) -> None:
        """
        Checks interactions between the given individual and other individuals at route intersections.

        Args:
            individual (Person): The individual whose interactions are being checked.
        """
        # Check people with intersections, calculate if touching and subject person to probability of getting infected
        if individual.get_status() == "I":
            for other in self.__route_intersections[individual.get_person_id()]:
                if (other.get_status() == "S" and
                    self.__calculate_distance(individual.get_current_position(),
                                              other.get_current_position()) <= 2 * individual.get_radius()):
                    if self.__disease.infect():
                        other.set_status("E")

    def __check_building_interactions(self) -> None:
        """
        Checks interactions between individuals in the same building (home or office).
        """
        for individual in self.__people:
            if individual.get_status() == "I":
                occupants = []
                # If individual at home, occupants are people in the house
                if individual.get_current_position() == individual.get_home_position():
                    occupants = self.__tilemap.get_home_from_location(individual.get_home_location()).get_occupants()
                # If individual at office, occupants are people in the office
                elif individual.get_current_position() == individual.get_office_position():
                    occupants = self.__tilemap.get_office_from_location(individual.get_office_location()).get_occupants()

                # Chance of those in same building getting infected
                for occupant in occupants:
                    if occupant.get_status() == "S" and self.__disease.infect():
                        occupant.set_status("E")

    def __calculate_distance(self, pos1: tuple[int, int], pos2: tuple[int, int]) -> float:
        """
        Calculates the distance between two positions.

        Args:
            pos1 (tuple[int, int]): The first position.
            pos2 (tuple[int, int]): The second position.

        Returns:
            float: The distance between the two positions.
        """
        return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)
