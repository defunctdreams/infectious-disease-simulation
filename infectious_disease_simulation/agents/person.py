"""
Defines the Person class which manages a person in the simulation.

Imports:
    math
    pygame
    display: Manages display settings and updates.
    disease: Simulates disease probabilities.

Classes:
    Person
"""
import math
import pygame
from ..display import pygame_display # For typing
from ..simulation import disease # For typing

class Person:
    """
    A class to manage a person in the simulation, including their movement and infection status.

    Attributes:
        __display (display.Display): The display surface.
        __person_id (int): The ID of the person.
        __home_location (tuple[int, int]): The home location of the person.
        __office_location (tuple[int, int]): The office location of the person.
        __current_location (tuple[int, int]): The current location of the person.
        __home_position (tuple[int, int]): The position within the home.
        __office_position (tuple[int, int]): The position within the office.
        __current_position (tuple[int, int]): The current position of the person.
        __home_radius (int): The radius of the person in their home.
        __office_radius (int): The radius of the person in their office.
        __home_to_office_route (list[tuple[int, int]]): The route from home to office.
        __office_to_home_route (list[tuple[int, int]]): The route from office to home.
        __speed (float): The speed of the person.
        __leave_home (int): The time to leave home.
        __status (str): The infection status of the person ('S', 'E', 'I', 'R', 'D').
        __route (list[tuple[int, int]]): The current route.
        __route_index (int): The index of the current position in the route.
        __moving (bool): Whether the person is moving.
        __disease (disease.Disease): The disease object managing infection.
        __incubation_time (float): The incubation time remaining for the person before becoming infectious.
        __seconds_per_hour (float): The number of seconds per simulation hour.
    """
    def __init__(self, display_obj: pygame_display.Display,
                 person_id: int,
                 home_location: tuple[int, int], office_location: tuple[int, int], home_position: tuple[int, int],
                 home_radius: int, office_radius: int,
                 home_to_office_route: list[tuple[int, int]],
                 speed: float, leave_home: int, status: str,
                 disease_obj: disease.Disease, incubation_time: float,
                 seconds_per_hour: float) -> None:
        """
        Initialises the Person class with the given parameters.

        Args:
            display_obj (display.Display): The display surface.
            person_id (int): The ID of the person.
            home_location (tuple[int, int]): The home location of the person.
            office_location (tuple[int, int]): The office location of the person.
            home_position (tuple[int, int]): The position within the home.
            home_radius (int): The radius of the home.
            office_radius (int): The radius of the office.
            home_to_office_route (list[tuple[int, int]]): The route from home to office.
            speed (float): The speed of the person.
            leave_home (int): The time to leave home.
            status (str): The infection status of the person.
            disease_obj (disease.Disease): The disease object managing infection.
            incubation_time (float): The incubation time for the disease.
            seconds_per_hour (float): The number of seconds per simulation hour.
        """
        self.__display: pygame_display.Display = display_obj
        self.__person_id: int = person_id
        self.__home_location: tuple[int, int] = home_location
        self.__office_location: tuple[int, int] = office_location
        self.__current_location: tuple[int, int] = self.__home_location
        self.__home_position: tuple[int, int] = home_position
        self.__office_position: tuple[int, int] = None
        self.__current_position: tuple[int, int] = self.__home_position
        self.__home_radius: int = home_radius
        self.__office_radius: int = office_radius
        self.__home_to_office_route: list[tuple[int, int]] = home_to_office_route
        self.__office_to_home_route: list[tuple[int, int]] = None
        self.__speed: float = speed
        self.__leave_home: int = leave_home
        self.__status: str = status  # S = Susceptible, E = Exposed, I = Infected, R = Recovered, D = Deceased
        self.__route: list[tuple[int, int]] = None
        self.__route_index: int = 0
        self.__moving: bool = False
        self.__disease: disease.Disease = disease_obj
        self.__incubation_time: float = incubation_time
        self.__seconds_per_hour: float = seconds_per_hour

    def draw_person(self) -> None:
        """
        Draws the person as a circle on the display surface.
        """
        pygame.draw.circle(self.__display.get_screen(),
                           self.get_colour(),
                           (int(self.__current_position[0]), int(self.__current_position[1])),
                           self.get_radius())

    def get_leave_home(self) -> int:
        """
        Gets the time to leave home.

        Returns:
            int: The time to leave home.
        """
        return self.__leave_home

    def get_home_location(self) -> tuple[int, int]:
        """
        Gets the home location of the person.

        Returns:
            tuple[int, int]: The home location.
        """
        return self.__home_location

    def get_office_location(self) -> tuple[int, int]:
        """
        Gets the office location of the person.

        Returns:
            tuple[int, int]: The office location.
        """
        return self.__office_location

    def get_current_location(self) -> tuple[int, int]:
        """
        Gets the current location of the person.

        Returns:
            tuple[int, int]: The current location.
        """
        return self.__current_location

    def set_current_location(self, new_location: tuple[int, int]) -> None:
        """
        Sets the current location of the person.

        Args:
            new_location (tuple[int, int]): The new location of the person.
        """
        self.__current_location = new_location

    def get_home_position(self) -> tuple[int, int]:
        """
        Gets the home position of the person.

        Returns:
            tuple[int, int]: The home position of the person.
        """
        return self.__home_position

    def get_office_position(self) -> tuple[int, int]:
        """
        Gets the office position of the person.

        Returns:
            tuple[int, int]: The office position of the person.
        """
        return self.__office_position

    def set_office_position(self, office_position: tuple[int, int]) -> None:
        """
        Sets the office position of the person and updates the route from home to office.

        Args:
            office_position (tuple[int, int]): The new office position of the person.
        """
        self.__office_position = office_position
        self.__home_to_office_route.insert(0, self.__home_position)
        self.__home_to_office_route.append(office_position)
        self.__office_to_home_route = list(reversed(self.__home_to_office_route))

    def get_current_position(self) -> tuple[int, int]:
        """
        Gets the current position of the person.

        Returns:
            tuple[int, int]: The current position of the person.
        """
        return self.__current_position

    def set_current_position(self, new_position: tuple[int, int]) -> None:
        """
        Sets the current position of the person.

        Args:
            new_position (tuple[int, int]): The new position of the person.
        """
        self.__current_position = new_position

    def get_radius(self) -> int:
        """
        Gets the radius corresponding to the current position of the person.

        Returns:
            int: The corresponding to the current position of the person.
        """
        if self.__current_position == self.__home_position:
            return self.__home_radius
        return self.__office_radius

    def get_colour(self) -> tuple[int, int, int]:
        """
        Gets the color representing the infection status of the person.

        Returns:
            tuple[int, int, int]: The RGB color based on the infection status.
        """
        status_colours = {
            "S": (144, 238, 144),  # Green
            "E": (255, 255, 0),    # Yellow
            "I": (255, 0, 0),      # Red
            "R": (204, 153, 255),  # Light Purple
            "D": (50, 50, 50)      # Dark Grey
        }
        return status_colours[self.__status]

    def start_move_to_office(self) -> None:
        """
        Starts the movement from home to the office if the person is not deceased.
        """
        if self.__status != 'D':
            self.__route = self.__home_to_office_route
            self.__route_index = 0
            self.__moving = True

    def start_move_to_home(self) -> None:
        """
        Starts the movement from the office to home if the person is not deceased.
        """
        if self.__status != 'D':
            self.__route = self.__office_to_home_route
            self.__route_index = 0
            self.__moving = True

    def update_position(self) -> None:
        """
        Updates the position of the person based on their route and speed. Stops moving if the person is deceased.

        If the person is moving, the position is updated along the route. If the person reaches the next position
        in the route, the route index is incremented. If the person reaches the end of the route, they stop moving.
        """
        if self.__status == 'D':
            self.__moving = False
            self.draw_person()
            return

        if self.__moving and self.__route_index < len(self.__route):
            next_position: tuple[int, int] = self.__route[self.__route_index]
            dx: float = next_position[0] - self.__current_position[0]
            dy: float = next_position[1] - self.__current_position[1]
            distance: float = math.sqrt(dx ** 2 + dy ** 2)
            # Adjust speed for smooth movement and avoid overshooting next position
            if distance < self.__speed:
                self.__current_position = next_position
                self.__route_index += 1
                if self.__route_index >= len(self.__route):
                    self.__moving = False
            else:
                dx = dx / distance * self.__speed
                dy = dy / distance * self.__speed
                self.__current_position = (self.__current_position[0] + dx, self.__current_position[1] + dy)

    def update_infection_status(self) -> None:
        """
        Updates the infection status of the person based on disease progression.

        If the person is exposed, the incubation time is decreased. If the incubation time reaches zero, the status
        changes to infected. If the person is infected, their status may change to recovered or deceased based on
        the disease recovery and mortality rates.
        """
        if self.__status == "E":
            self.__incubation_time -= self.__seconds_per_hour  # Decrease incubation time
            if self.__incubation_time <= 0: # Set to infected once incubation time left reaches 0
                self.__status = "I"
        elif self.__status == "I":
            if self.__disease.recover(): # Probability of recovering
                self.__status = "R"
            elif self.__disease.die(): # Probability of dying
                self.__status = "D"
                self.__moving = False

    def get_status(self) -> str:
        """
        Gets the current infection status of the person.

        Returns:
            str: The current infection status (S, E, I, R, D).
        """
        return self.__status

    def set_status(self, status: str) -> None:
        """
        Sets the infection status of the person.

        Args:
            status (str): The new infection status (S, E, I, R, D).
        """
        self.__status = status

    def get_person_id(self) -> int:
        """
        Gets the ID of the person.

        Returns:
            int: The ID of the person.
        """
        return self.__person_id

    def get_home_to_office_route(self) -> list[tuple[int, int]]:
        """
        Gets the route from home to office.

        Returns:
            list[tuple[int, int]]: The route from home to office.
        """
        return self.__home_to_office_route
