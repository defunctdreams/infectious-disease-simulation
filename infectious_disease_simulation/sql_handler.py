"""
Defines the SQLHandler class to manage database interactions.

Imports:
    sqlite3
    datetime

Classes:
    SQLHandler
"""
import sqlite3
import datetime

class SQLHandler:
    """
    A class to handle SQLite database interactions for saving simulation parameters.

    Attributes:
        __connection (sqlite3.Connection): The SQLite database connection.
    """
    def __init__(self, db_name: str = 'simulation_params.db') -> None:
        """
        Initialises the SQLHandler class by creating a database connection and table.

        Args:
            db_name (str): The name of the database file. Defaults to 'simulation_params.db'.
        """
        self.__connection: sqlite3.Connection = self.__create_connection(db_name)
        self.__create_table()

    def __create_connection(self, db_name: str) -> sqlite3.Connection:
        """
        Creates a connection to the SQLite database.

        Args:
            db_name (str): The name of the database file.

        Returns:
            sqlite3.Connection: The database connection.
        """
        connection: sqlite3.connect = None

        # Error handling
        try:
            connection = sqlite3.connect(db_name)
        except sqlite3.Error as error:
            print(f"The error '{error}' occurred")
        return connection

    def __create_table(self) -> None:
        """
        Creates the 'simulations' table in the database if it does not already exist.
        """
        create_table_query = """
        CREATE TABLE IF NOT EXISTS simulations (
            run_id INTEGER PRIMARY KEY AUTOINCREMENT,
            datetime TEXT NOT NULL,
            simulation_name TEXT NOT NULL,
            simulation_speed REAL NOT NULL,
            display_size INTEGER NOT NULL,
            num_houses INTEGER NOT NULL,
            num_offices INTEGER NOT NULL,
            building_size INTEGER NOT NULL,
            num_people_in_house INTEGER NOT NULL,
            show_drawing INTEGER NOT NULL,
            additional_roads INTEGER NOT NULL,
            infection_rate REAL NOT NULL,
            incubation_time REAL NOT NULL,
            recovery_rate REAL NOT NULL,
            mortality_rate REAL NOT NULL
        );
        """

        # Error handling
        try:
            cursor = self.__connection.cursor()
            cursor.execute(create_table_query)
            self.__connection.commit()
        except sqlite3.Error as error:
            print(f"The error '{error}' occurred")

    def save_params(self, params: tuple) -> None:
        """
        Saves the simulation parameters to the database.

        Args:
            params (tuple): The simulation parameters to save.
        """
        datetime_str: str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Current datetime
        parameters = (datetime_str, *params) # Required parameters, unpacks params

        save_query = """
        INSERT INTO simulations (datetime, simulation_name, simulation_speed, display_size, num_houses, num_offices, 
        building_size, num_people_in_house, show_drawing, additional_roads, infection_rate, 
        incubation_time, recovery_rate, mortality_rate) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        cursor = self.__connection.cursor()
        cursor.execute(save_query, parameters)
        self.__connection.commit()

    def close_connection(self) -> None:
        """
        Closes the database connection.
        """
        if self.__connection:
            self.__connection.close()
