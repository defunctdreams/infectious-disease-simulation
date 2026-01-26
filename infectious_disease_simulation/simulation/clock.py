"""
Manages and displays time within the simulation and updates relevant parts of the simulation.

Imports:
    time
    pygame
    display: Manages display properties and pygame modules for handling the display.
    population: Manages general methods relevant to the whole population. Also calls for people to be initialised.
    plot_graph: Manages the display of simulation data in graph form.

Classes:
    Clock
"""

import time
import pygame
from ..display import pygame_display # For typing
from ..simulation import population # For typing
from ..viz import plot_graph

class Clock:
    """
    A class to manage and display time within a simulation.

    Attributes:
        __day (int): The current day of the simulation.
        __hour (int): The current hour of the simulation.
        __running (bool): The state of the simulation (running or not).
        __seconds_per_hour (float): The number of real-world seconds per simulation hour.
        __fps (int): The frames per second for the simulation display.
        __font (pygame.font.Font): The font used to display time.
        __display (display.Display): The display surface for the simulation.
        __population (population.Population): The population being simulated.
        __last_update (float): The last time the simulation was updated.
        __graph (plot_graph.PlotGraph): The graph to display simulation data.
    """
    def __init__(self, display_obj: pygame_display.Display,
                 population_obj: population.Population,
                 seconds_per_hour: float, fps: int) -> None:
        """
        Initialises the Clock class with the given parameters.

        Args:
            display_obj (display.Display): The display surface for the simulation.
            population_obj (population.Population): The population being simulated.
            seconds_per_hour (int): The number of real-world seconds per simulation hour.
            fps (int): The frames per second for the simulation display.
        """
        self.__day: int = 1
        self.__hour: int = 0
        self.__running: bool = True
        self.__seconds_per_hour: float = seconds_per_hour
        self.__fps: int = fps
        pygame.font.init()
        self.__font: pygame.font.Font = pygame.font.SysFont('Arial Bold', 25)
        self.__display: pygame_display.Display = display_obj
        self.__population: population.Population = population_obj
        self.__last_update: float = time.time()
        self.__graph: plot_graph.PlotGraph = plot_graph.PlotGraph(self.__display.get_caption(), self.__fps)
        self.__graph.update(self.__day, self.__hour, self.__population.get_status_counts())

    def update_time(self) -> None:
        """
        Updates the time within the simulation. Stops the simulation if there are no active infections.
        """
        if not self.__running: # Stop if not running
            return

        if not self.__population.has_active_infections(): # If no infections, update graph and stop running
            self.__population.update_infection_status()
            counts = self.__population.get_status_counts()
            self.__graph.update(self.__day, self.__hour, counts)
            self.__running = False
            return

        current_time: float = time.time()

        # If a simulation hour has passed
        if current_time - self.__last_update >= self.__seconds_per_hour:
            self.__hour += 1 # Increment simulation hour
            self.__population.update_infection_status() # Update infections

            counts = self.__population.get_status_counts()
            self.__graph.update(self.__day, self.__hour, counts) # Update graph with current population status

            if self.__hour > 24: # Change day
                self.__hour = 1
                self.__day += 1

            # People to reach office by hour 9 and leave by hour 17
            for individual in self.__population.get_people():
                if self.__hour == individual.get_leave_home():
                    individual.start_move_to_office()
                elif self.__hour == 17:
                    individual.start_move_to_home()

            self.__last_update = current_time

    def display_time(self) -> None:
        """
        Displays the current time on the simulation display.
        """
        if self.__running:
            time_text: str = f"Day: {self.__day}, Hour: {self.__hour}"
        else:
            time_text: str = "Simulation Ended"

        text_surface: pygame_display.Display = self.__font.render(time_text, True, (0, 0, 0))
        self.__display.get_screen().blit(text_surface, (10, 10))

    def get_running(self) -> bool:
        """
        Gets the running state of the simulation.

        Returns:
            bool: True if the simulation is running, False otherwise.
        """
        return self.__running
