"""
Main module to initialise and run the simulation.

Imports:
    pygame
    interface: Manages the simulation parameters interface.
    sql_handler: Handles SQL database interactions.
    display: Manages display settings and updates.
    create_map: Creates and manages the simulation map.
    disease: Simulates disease probabilities.
    population: Manages the population within the simulation.
    clock: Manages updating the simulation clock.

Classes:
    Main
"""

import pygame
import os
import sys
from .ui.interface import Interface
from .display import Display
from .world import create_map
from .simulation import disease
from .simulation import population
from .simulation import clock
from .config import Config
from .errors import ConfigError, DBError
from .storage.db_handler import DBHandler

class Main:
    """
    Main class to initialise and run the simulation.

    Attributes:
        __interface (interface.Interface): Handles user interface of the program.
        __params (dict[str, any]): The user-entered parameters for the program to use and run.
        __sql_handler (sql_handler.SQLHandler): Handles connections, queries, and anything related to SQL.
        __seconds_per_hour (float): The number of seconds per simulation hour.
        __fps (int): The number of display updates per second.
        __display (display.Display): The display object, containing properties and modules for managing the display.
        __map_surface (pygame.Surface): A separate object for the map.
        __map (create_map.CreateMap): Object which handles the map generation.
        __disease (disease.Disease): Handles the disease properties and probability of person moving between states.
        __population (population.Population): Handles the initialisation of the population.
        __clock (clock.Clock): Manages the simulation clock which starts people movement, initialises the live graph.
    """
    def __init__(self) -> None:
        """
        Initialises the Main class, sets up interface, parameters, display, map, disease, population, and clock.
        Runs the simulation if parameters are valid.
        """
        headless = "--headless" in sys.argv
        if headless:
            sys.argv.remove("--headless")

        # Pulls database name
        db_name: str = self.__get_db_name()

        # Initialise interface and get parameters
        ui = Interface(db_name)
        self.__config = ui.get_config()

        if self.__config is None:
            return  # User closed the window


        # Initialise class to handle SQL queries
        try:
            with DBHandler(db_name) as db_handler:
                db_handler.save_params(self.__config)
            print("Parameters saved successfully.")
        except DBError as e:
            print(f"Error while saving parameters: {e}")

        # Configure timescales
        self.__seconds_per_hour: float = 1 / self.__config.simulation_speed
        self.__fps: int = 60

        # Initialise display with parameters
        self.__display: Display = Display(self.__config.display_size,
                                          self.__config.display_size,
                                          self.__config.simulation_name,
                                          headless)
        self.__initialise_display()

        # Create a separate surface for the map, intialise and draw map with parameters
        self.__map_surface: pygame.Surface = pygame.Surface((self.__display.get_width(), self.__display.get_height()))
        self.__map: create_map.CreateMap = create_map.CreateMap(self.__display,
                                                               self.__config.num_houses,
                                                               self.__config.num_offices,
                                                               self.__config.building_size,
                                                               self.__config.building_size)
        self.__map.draw(self.__config.show_drawing, self.__config.additional_roads)

        # Draw map onto map surface
        self.__map_surface.blit(self.__display.get_screen(), (0, 0))

        # Initialise disease with parameters
        self.__disease: disease.Disease = disease.Disease(self.__config.infection_rate,
                                                          self.__config.incubation_time,
                                                          self.__config.recovery_rate,
                                                          self.__config.mortality_rate,
                                                          self.__seconds_per_hour)

        # Initialise population with parameters
        print("Initialising Population...")
        self.__population: population.Population = population.Population(self.__config.num_people_in_house,
                                                                         self.__display,
                                                                         self.__map,
                                                                         self.__disease,
                                                                         self.__seconds_per_hour,
                                                                         self.__fps)

        # Initialise clock with parameters
        self.__clock: clock.Clock = clock.Clock(self.__display, self.__population, self.__seconds_per_hour, self.__fps)

        # Run simulation
        print("Running Simulation...")
        self.__run_simulation()

    def __initialise_display(self) -> None:
        """
        Initialises the display by setting the caption, filling the background, and setting the display icon.
        """
        self.__display.set_caption()
        self.__display.fill((255, 255, 255))
        self.__display.set_display_icon("images\\virus_icon.png")

    def __run_simulation(self) -> None:
        """
        Runs the simulation by updating time, positions, and rendering the display in a loop until window is closed.
        """
        running: bool = True # Flag for running
        pygame_clock: pygame.time.Clock = pygame.time.Clock()

        # Enter simulation loop
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # Handle quitting
                    running = False

            if self.__clock.get_running():
                self.__clock.update_time() # Update simulation time
                self.__population.update_positions() # Update people's positions
                self.__display.get_screen().blit(self.__map_surface, (0, 0)) # Map surface as 'background'
                self.__population.draw_people() # Draw people
            
            self.__clock.display_time() # Draw the clock on top
            self.__display.update()
            pygame_clock.tick(self.__fps) # Update required parts every frame
        pygame.quit()

    def __get_db_name(self, db_name: str = "simulation_params.db") -> str:
        """
        Checks where XDG_CONFIG_HOME is, taken from https://cgit.freedesktop.org/xdg/pyxdg/tree/xdg/BaseDirectory.py
        
        Args:
            db_name (str): The name of the database file. Defaults to 'simulation_params.db'.

        Returns:
            str: The databases full path
        """

        _home = os.path.expanduser('~')
        xdg_data_home = os.environ.get('XDG_DATA_HOME') or \
            os.path.join(_home, '.local', 'share')
        dir_path = os.path.join(xdg_data_home, "infectious-disease-simulation")

        try:
            os.makedirs(dir_path) # Only on first run
        except FileExistsError:
            pass # This just means the directory is already there which will happen for all subsequent runs
        except Exception as err:
            print(f"An error occurred: {err}") # Any other error we just put db in current dir
            dir_path = os.path.curdir

        new_path = os.path.join(dir_path, db_name)
        return str(new_path)

# Run the main program
if __name__ == "__main__":
    Main()
