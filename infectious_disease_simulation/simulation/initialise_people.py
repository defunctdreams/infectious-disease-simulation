"""
Initialises people and their properties within a simulation.

Imports:
    random
    math
    display: Manages display settings and updates.
    tilemap: Creates the tilemap of buildings.
    create_map: Creates and manages the simulation map.
    disease: Simulates disease probabilities.
    person: Manages and holds a simulated person's properties and person-specific methods.
    dijkstra: Implements Dijkstra's algorithm for finding the shortest path.

Classes:
    InitialisePeople
"""

import random
import math
from ..display import Display # For typing
from ..world import tilemap # For typing
from ..world import create_map # For typing
from ..simulation import disease # For typing
from ..agents import person
from ..agents import dijkstra

class InitialisePeople:
    """
    A class to initialise people and their properties within a simulation.

    Attributes:
        __display (display.Display): The display surface.
        __map (create_map.CreateMap): The map object managing roads.
        __tilemap (tilemap.Tilemap): The tilemap object managing buildings on the map.
        __disease (disease.Disease): The disease object for infection simulation.
        __num_in_house (int): Number of people per house.
        __seconds_per_hour (float): The number of seconds per simulation hour.
        __fps (int): The frames per second for the simulation.
        __roads (dict[tuple[int, int], list[tuple[tuple[int, int], int]]]): The dictionary of roads.
        __building_width (int): The width of the buildings.
        __building_height (int): The height of the buildings.
        __dijkstra (dijkstra.Dijkstra): Dijkstra for pathfinding.
        __people (list[person.Person]): The list of Person objects initialised.
    """
    def __init__(self, num_in_house: int,
                 display_obj: Display, map_obj: create_map.CreateMap, disease_obj: disease.Disease,
                 seconds_per_hour: float, fps: int) -> None:
        """
        Initialises the InitialisePeople class with the given parameters.

        Args:
            num_in_house (int): Number of people per house.
            display_obj (display.Display): The display surface.
            map_obj (create_map.CreateMap): The map object managing roads.
            disease_obj (disease.Disease): The disease object for infection simulation.
            seconds_per_hour (float): The number of seconds per simulation hour.
            fps (int): The frames per second for the simulation.
        """
        self.__display: Display = display_obj
        self.__map: create_map.CreateMap = map_obj
        self.__tilemap: tilemap.Tilemap = self.__map.get_tilemap()
        self.__disease: disease.Disease = disease_obj
        self.__num_in_house: int = num_in_house
        self.__seconds_per_hour: float = seconds_per_hour
        self.__fps: int = fps
        self.__delta_time: float = 1 / self.__fps
        self.__roads: dict[tuple[int, int], list[tuple[tuple[int, int], int]]] = self.__map.get_roads()
        self.__building_width: int = self.__tilemap.get_building_width()
        self.__building_height: int = self.__tilemap.get_building_height()
        self.__dijkstra: dijkstra.Dijkstra = dijkstra.Dijkstra(self.__roads)
        self.__people: list[person.Person] = self.__initialise_people()

    def get_people(self) -> list[person.Person]:
        """
        Gets the list of people.

        Returns:
            list[person.Person]: The list of person objects initialised.
        """
        return self.__people

    def __initialise_people(self) -> list[person.Person]:
        """
        Initialises people in the houses on the tilemap.

        Returns:
            list[person.Person]: The list of person objects initialised.
        """
        people: list[person.Person] = [] # Initialise list

        # Get required values
        num_people: int = self.__tilemap.get_num_houses() * self.__num_in_house
        infected_person_id: int = random.randint(0, num_people - 1)
        office_location_dist: list[tuple[int, int]] = self.__calculate_office_location_dist(num_people)
        random.shuffle(office_location_dist)
        office_location_dist_dict: dict[tuple[int, int], int] = self.__convert_list_to_dict(office_location_dist)

        # Calculate and set values for each person's parameters
        for person_id in range(num_people):
            home_location: tuple[int, int] = self.__calculate_home_location(person_id, self.__num_in_house)
            office_location: tuple[int, int] = self.__calculate_office_location(person_id, office_location_dist)
            home_position: tuple[int, int] = self.__calculate_home_position(person_id, self.__num_in_house, home_location)
            home_radius: int = self.__calculate_radius(self.__num_in_house)
            office_radius: int = self.__calculate_radius(office_location_dist_dict[office_location])
            home_to_office_route, route_weight = self.__dijkstra.compute(home_location, office_location)
            home_to_office_route: list[tuple[int, int]] = self.__scale_xy_list(home_to_office_route)
            speed: float = self.__calculate_speed()
            time_to_travel: float = self.__calculate_time_to_travel((route_weight + 0.5), speed)
            leave_home: int = self.__calculate_leave_home(time_to_travel)
            status: str = self.__calculate_status(person_id, infected_person_id)

            individual: person.Person = person.Person(self.__display, person_id,
                                       home_location, office_location, home_position,
                                       home_radius, office_radius,
                                       home_to_office_route, speed, leave_home, status,
                                       self.__disease, self.__disease.get_incubation_time(),
                                       self.__seconds_per_hour, self.__delta_time)

            self.__tilemap.get_home_from_location(home_location).add_occupant(individual)
            self.__tilemap.get_office_from_location(office_location).add_occupant(individual)
            individual.set_office_position(self.__calculate_office_position(person_id,
                                                                            office_location,
                                                                            office_location_dist_dict))

            people.append(individual) # Add person to list of people

        return people

    def __calculate_status(self, person_id: int, infected_person_id: int) -> str:
        """
        Calculates the initial status of a person.

        Args:
            person_id (int): The ID of the person.
            infected_person_id (int): The ID of the initially infected person.

        Returns:
            str: 'I' if the person is infected, 'S' if susceptible.
        """
        if person_id == infected_person_id:
            return 'I'
        return 'S'

    def __calculate_leave_home(self, time_to_travel: float) -> int:
        """
        Calculates the time to leave home for work so person reaches at 9am.

        Args:
            time_to_travel (float): The time it takes to travel to work.

        Returns:
            int: The hour to leave home.
        """
        leave_home: int = 9 - math.ceil(time_to_travel)# - 1
        if leave_home < 1:
            return 1
        return leave_home

    def __calculate_time_to_travel(self, route_weight: float, speed: float) -> float:
        """
        Calculates the time to travel a given route.

        Args:
            route_weight (float): The weight of the route.
            speed (float): The speed of travel.

        Returns:
            float: The time to travel the route.
        """
        return math.ceil(((route_weight) / speed)) / self.__seconds_per_hour

    def __calculate_speed(self) -> float:
        """
        Calculates the speed of travel.

        Returns:
            float: The speed of travel.
        """
        return math.floor((self.__display.get_width() * (60 / self.__fps))
                          /
                          ((2 * self.__building_width) * self.__seconds_per_hour))

    def __scale_xy_list(self, xylist: list[tuple[int, int]]) -> list[tuple[int, int]]:
        """
        Scales a list of x, y coordinates to fit the display.

        Args:
            xylist (list[tuple[int, int]]): The list of x, y coordinates.

        Returns:
            list[tuple[int, int]]: The scaled list of x, y coordinates.
        """
        scaled_xy_list: list[tuple[int, int]] = []

        # Scale so x, y tilemap locations are in the right place on the display
        for x, y in xylist:
            scaled_x: int = x * self.__building_width + self.__building_width // 2
            scaled_y: int = y * self.__building_height + self.__building_height // 2
            scaled_xy_list.append((scaled_x, scaled_y))

        return scaled_xy_list

    def __calculate_home_location(self, person_id: int, num_in_house: int) -> tuple[int, int]:
        """
        Calculates the home location for a person.

        Args:
            person_id (int): The ID of the person.
            num_in_house (int): Number of people per house.

        Returns:
            tuple[int, int]: The home location.
        """
        # Home locations set by person_id
        home_location: tuple[int, int] = self.__tilemap.get_houses()[person_id // num_in_house].get_location()
        return home_location

    def __calculate_office_location(self, person_id: int,
                                    office_location_dist: list[tuple[int, int]]) -> tuple[int, int]:
        """
        Calculates the office location for a person.

        Args:
            person_id (int): The ID of the person.
            office_location_dist (list[tuple[int, int]]): The list of office locations.

        Returns:
            tuple[int, int]: The office location.
        """
        office_location: tuple[int, int] = office_location_dist[person_id]
        return office_location

    def __calculate_home_position(self, person_id: int,
                                  num_in_house: int,
                                  home_location: tuple[int, int]) -> tuple[int, int]:
        """
        Calculates the home position for a person within their house.

        Args:
            person_id (int): The ID of the person.
            num_in_house (int): Number of people per house.
            home_location (tuple[int, int]): The location of the house.

        Returns:
            tuple[int, int]: The home position within the house.
        """
        positions: list[tuple[int, int]] = self.__calculate_positions(num_in_house, home_location)
        home_position: tuple[int, int] = positions[person_id % num_in_house]
        return home_position

    def __calculate_office_position(self, person_id: int,
                                    office_location: tuple[int, int],
                                    office_location_dist_dict: dict[tuple[int, int], int]) -> tuple[int, int]:
        """
        Calculates the office position for a person within their office.

        Args:
            person_id (int): The ID of the person.
            office_location (tuple[int, int]): The location of the office.
            office_location_dist_dict (dict[tuple[int, int], int]): The dictionary of office locations and counts.

        Returns:
            tuple[int, int]: The office position within the office.
        """
        num_in_office: int = office_location_dist_dict[office_location]
        positions: list[tuple[int, int]] = self.__calculate_positions(num_in_office, office_location)
        occupants: list[person.Person] = self.__tilemap.get_office_from_location(office_location).get_occupants()
        occupant_index: int | None = None

        # Get person's occupant_index in occupants of office so office position can be calculated
        for index, individual in enumerate(occupants):
            if individual.get_person_id() == person_id:
                occupant_index = index
                break

        if occupant_index is None:
            raise RuntimeError(f"Person ID {person_id} not found in occupants of office at location {office_location}")

        # Place in position depending on occupant index in positions to ensure no same positions.
        office_position: tuple[int, int] = positions[occupant_index]

        return office_position

    def __calculate_office_location_dist(self, num_people: int) -> list[tuple[int, int]]:
        """
        Calculates the distribution of office locations for people.

        Args:
            num_people (int): The number of people.

        Returns:
            list[tuple[int, int]]: The list of office locations for people.
        """
        office_location_dist: list[tuple[int, int]] = []
        num_offices: int = len(self.__tilemap.get_offices())
        people_dist_in_offices: list[int] = self.__calculate_people_dist_in_offices(num_people, num_offices)

        # Iterate through to add the distribution of offices to list
        for index, num in enumerate(people_dist_in_offices):
            office_location: tuple[int, int] = self.__tilemap.get_offices()[index].get_location()
            for _ in range(num):
                office_location_dist.append(office_location)

        return office_location_dist

    def __calculate_people_dist_in_offices(self, num_people: int, num_offices: int) -> list[int]:
        """
        Calculates the distribution of people across offices.

        Args:
            num_people (int): The number of people.
            num_offices (int): The number of offices.

        Returns:
            list[int]: The list of people count per office.
        """
        base_allocation: int = num_people // num_offices # Num people per office if everyone could be evenly distributed
        extra_people: int = num_people % num_offices # Remainder of people not considered in base_allocation

        distribution: list[int] = [base_allocation] * num_offices # Distribution list with num_office elements of base_allocation

        for i in range(extra_people): # Increments the first extra_people elements of distribution by 1 for even spread
            distribution[i] += 1

        return distribution

    def __calculate_positions(self, num_in_building: int, building_location: tuple[int, int]) -> list[tuple[int, int]]:
        """
        Calculates positions for people within a building.

        Args:
            num_in_building (int): The number of people in the building.
            building_location (tuple[int, int]): The location of the building.

        Returns:
            list[tuple[int, int]]: The list of positions within the building.
        """
        # Divide building into divisions of squares depending on number of people in building
        divisions: int = math.ceil(math.sqrt(num_in_building))
        x_location, y_location = building_location

        # Calculate the offset for displaying people without overlaps
        x_offset: float = self.__building_width / (divisions + 1)
        y_offset: float = self.__building_height / (divisions + 1)
        positions: list[tuple[int, int]] = []

        # Loop through possible offsets and add to list of positions
        for i in range(divisions):
            col: int = i + 1
            for j in range(divisions):
                row: int = j + 1
                x: int = round((x_location * self.__building_width) + (x_offset * row))
                y: int = round((y_location * self.__building_height) + (y_offset * col))
                positions.append((x, y))

        return positions

    def __convert_list_to_dict(self, input_list: list[tuple[int, int]]) -> dict[tuple[int, int], int]:
        """
        Converts a list to a dictionary with counts of each item.

        Args:
            input_list (list[tuple[int, int]]): The input list.

        Returns:
            dict[tuple[int, int], int]: The dictionary with counts of each item.
        """
        dictionary: dict[tuple[int, int], int] = {}

        for key in input_list:
            if key in dictionary:
                dictionary[key] += 1
            else:
                dictionary[key] = 1

        return dictionary

    def __calculate_radius(self, num_in_building: int) -> int:
        """
        Calculates the radius for people within a building so they can be displayed easily.

        Args:
            num_in_building (int): The number of people in the building.

        Returns:
            int: The radius.
        """
        default_radius: int = min(self.__building_width, self.__building_height) // 10
        # Determine layour divisions (grid) and derive radius so items fit
        divisions: int = math.ceil(math.sqrt(num_in_building))
        # Radius so everyone's radii fit exactly into building
        even_radius: int = min(self.__building_width, self.__building_height) // (2 * (divisions + 1))

        radius: int = min(default_radius, even_radius) # Smallest of the two
        return radius
