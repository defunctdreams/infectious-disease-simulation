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
from . import interface
from . import sql_handler
from . import display
from . import create_map
from . import disease
from . import population
from . import clock

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
        # Pulls database name
        db_name: str = self.__get_db_name()

        # Initialise interface and get parameters
        self.__interface: interface.Interface = interface.Interface(db_name)
        self.__params: dict[str, any] = self.__interface.get_params()

        # Initialise class to handle SQL queries
        self.__sql_handler: sql_handler.SQLHandler = sql_handler.SQLHandler(db_name)
        if self.__none_params(): # If parameters are returned as None (window closed), don't feed params into simulation
            return
        self.__save_params() # Save parameters into database
        self.__sql_handler.close_connection()
        print("Parameters saved successfully.")

        # Configure timescales
        self.__seconds_per_hour: float = 1 / self.__params['simulation_speed']
        self.__fps: int = 60

        # Initialise display with parameters
        self.__display: display.Display = display.Display(self.__params['display_size'],
                                                          self.__params['display_size'],
                                                          self.__params['simulation_name'])
        self.__initialise_display()

        # Create a separate surface for the map, intialise and draw map with parameters
        self.__map_surface: pygame.Surface = pygame.Surface((self.__display.get_width(), self.__display.get_height()))
        self.__map: create_map.CreateMap = create_map.CreateMap(self.__display,
                                                               self.__params['num_houses'],
                                                               self.__params['num_offices'],
                                                               self.__params['building_size'],
                                                               self.__params['building_size'])
        self.__map.draw(self.__params['show_drawing'], self.__params['additional_roads'])

        # Draw map onto map surface
        self.__map_surface.blit(self.__display.get_screen(), (0, 0))

        # Initialise disease with parameters
        self.__disease: disease.Disease = disease.Disease(self.__params['infection_rate'],
                                                          self.__params['incubation_time'],
                                                          self.__params['recovery_rate'],
                                                          self.__params['mortality_rate'],
                                                          self.__seconds_per_hour)

        # Initialise population with parameters
        print("Initialising Population...")
        self.__population: population.Population = population.Population(self.__params['num_people_in_house'],
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

    def __none_params(self) -> bool:
        """
        Checks if the parameters are None.

        Returns:
            bool: True if parameters are None, False otherwise.
        """
        if self.__params is None:
            return True
        return False

    def __save_params(self) -> None:
        """
        Saves the parameters to the database using SQLHandler.
        """
        # Get parameters and save in database
        params: tuple = (
            self.__params["simulation_name"], self.__params["simulation_speed"],
            self.__params["display_size"],
            self.__params["num_houses"], self.__params["num_offices"], self.__params["building_size"],
            self.__params["num_people_in_house"],
            self.__params["show_drawing"], self.__params["additional_roads"],
            self.__params["infection_rate"], self.__params["incubation_time"],
            self.__params["recovery_rate"], self.__params["mortality_rate"]
        )
        self.__sql_handler.save_params(params)

    def __initialise_display(self) -> None:
        """
        Initialises the display by setting the caption, filling the background, and setting the display icon.
        """
        self.__display.set_caption()
        self.__display.fill((255, 255, 255))
        self.__display.set_display_icon("infectious_disease_simulation/images/virus_icon.png")

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
        print(new_path)
        return str(new_path)

# Run the main program
if __name__ == "__main__":
    Main()
