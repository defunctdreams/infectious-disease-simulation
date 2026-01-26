"""
Interface for setting simulation parameters using a graphical user interface (GUI) built with Tkinter.

Imports:
    tkinter
    ttk
    messagebox
    sqlite3
    math

Classes:
    Interface
"""

import tkinter as tk
from tkinter import ttk, messagebox
import math
from ..config import Config
from ..errors import ConfigError, DBError
from ..storage.db_handler import DBHandler

class Interface:
    """
    A class to create and manage the simulation parameters interface.

    Attributes:
        __root (tk.Tk): The main window of the GUI.
        __style (ttk.Style): 
        __params (dict[str, any]): A dictionary to store user-entered simulation parameters.
    """
    def __init__(self, db_name: str) -> None:
        """
        Initialises the Interface class by setting up the main window and creating widgets.
        """
        self.__root: tk.Tk = tk.Tk()
        self.__root.title("Simulation Parameters")

        self.__style: ttk.Style = ttk.Style()
        self.__style.configure("TLabel", padding=6)

        self.__params: dict[str, any] = {}
        self.__config: Config | None = None

        self.__db_name: str = db_name

        self.__create_widgets(self.__db_name)
        self.__root.protocol("WM_DELETE_WINDOW", self.__on_closing)

        self.__load_window: tk.Toplevel | None = None

    def __create_widgets(self, db_name: str) -> None:
        """
        Creates and arranges the widgets for the simulation parameters interface.

        Args:
            db_name (str): The name of the database file.
        """
        # Simulation Name and Speed
        simulation_frame: ttk.LabelFrame = ttk.LabelFrame(self.__root, text="Simulation")
        simulation_frame.grid(row=0, columnspan=2, padx=10, pady=10, sticky="ew")

        ttk.Label(simulation_frame, text="Simulation Name:").grid(row=0, column=0, sticky="w")
        self.__params["simulation_name"] = ttk.Entry(simulation_frame)
        self.__params["simulation_name"].insert(0, "Simulation")
        self.__params["simulation_name"].grid(row=0, column=1, sticky="w")

        ttk.Label(simulation_frame, text="Simulation Speed:").grid(row=1, column=0, sticky="w")
        self.__simulation_speed: tk.DoubleVar = tk.DoubleVar(value=2)
        self.__simulation_speed_scale: ttk.Scale = ttk.Scale(
            simulation_frame, from_=0.5, to=5.0, variable=self.__simulation_speed, orient='horizontal',
            command=self.__update_speed_label, length=150
        )
        self.__simulation_speed_scale.grid(row=1, column=1, sticky="ew")
        self.__simulation_speed_label: ttk.Label = ttk.Label(simulation_frame, text="2x")
        self.__simulation_speed_label.grid(row=1, column=2, sticky="w")

        self.__simulation_speed_values: list[float] = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
        self.__simulation_speed_scale.set(self.__simulation_speed_values[3])

        # Display Parameters
        display_frame: ttk.LabelFrame = ttk.LabelFrame(self.__root, text="Display")
        display_frame.grid(row=1, columnspan=2, padx=10, pady=10, sticky="ew")

        ttk.Label(display_frame, text="Display Size (pixels):").grid(row=0, column=0, sticky="w")
        self.__params["display_size"] = ttk.Entry(display_frame)
        self.__params["display_size"].insert(0, "800")
        self.__params["display_size"].grid(row=0, column=1)

        # Map Parameters
        map_frame: ttk.LabelFrame = ttk.LabelFrame(self.__root, text="Map")
        map_frame.grid(row=2, columnspan=2, padx=10, pady=10, sticky="ew")

        ttk.Label(map_frame, text="Number of Houses:").grid(row=0, column=0, sticky="w")
        self.__params["num_houses"] = ttk.Entry(map_frame)
        self.__params["num_houses"].insert(0, "75")
        self.__params["num_houses"].grid(row=0, column=1)

        ttk.Label(map_frame, text="Number of Offices:").grid(row=1, column=0, sticky="w")
        self.__params["num_offices"] = ttk.Entry(map_frame)
        self.__params["num_offices"].insert(0, "25")
        self.__params["num_offices"].grid(row=1, column=1)

        ttk.Label(map_frame, text="Building Size (pixels):").grid(row=2, column=0, sticky="w")
        self.__params["building_size"] = ttk.Entry(map_frame)
        self.__params["building_size"].insert(0, "50")
        self.__params["building_size"].grid(row=2, column=1)

        # Population Parameters
        population_frame: ttk.LabelFrame = ttk.LabelFrame(self.__root, text="Population")
        population_frame.grid(row=3, columnspan=2, padx=10, pady=10, sticky="ew")

        ttk.Label(population_frame, text="Number of People per House:").grid(row=0, column=0, sticky="w")
        self.__params["num_people_in_house"] = ttk.Entry(population_frame)
        self.__params["num_people_in_house"].insert(0, "4")
        self.__params["num_people_in_house"].grid(row=0, column=1)

        # Map Drawing Parameters
        map_drawing_frame: ttk.Label = ttk.LabelFrame(self.__root, text="Map Drawing")
        map_drawing_frame.grid(row=4, columnspan=2, padx=10, pady=10, sticky="ew")

        self.__show_drawing: tk.BooleanVar = tk.BooleanVar(value=True)
        ttk.Checkbutton(map_drawing_frame, text="Show Map Drawing Process",
                        variable=self.__show_drawing).grid(row=0, columnspan=2, sticky="w")

        self.__additional_roads: tk.BooleanVar = tk.BooleanVar(value=True)
        ttk.Checkbutton(map_drawing_frame, text="Draw Additional Roads",
                        variable=self.__additional_roads).grid(row=1, columnspan=2, sticky="w")

        # Disease Parameters
        disease_frame: ttk.LabelFrame = ttk.LabelFrame(self.__root, text="Disease")
        disease_frame.grid(row=5, columnspan=2, padx=10, pady=10, sticky="ew")

        ttk.Label(disease_frame, text="Infection Rate:").grid(row=0, column=0, sticky="w")
        self.__params["infection_rate"] = ttk.Entry(disease_frame)
        self.__params["infection_rate"].insert(0, "0.7")
        self.__params["infection_rate"].grid(row=0, column=1)
        ttk.Label(disease_frame,
                  text="Probability of a contact getting infected. Decimal between 0 and 1.").grid(row=1,
                                                                                                   column=0,
                                                                                                   columnspan=2,
                                                                                                   sticky="w")

        ttk.Label(disease_frame, text="Incubation Time:").grid(row=2, column=0, sticky="w")
        self.__params["incubation_time"] = ttk.Entry(disease_frame)
        self.__params["incubation_time"].insert(0, "2.0")
        self.__params["incubation_time"].grid(row=2, column=1)
        ttk.Label(disease_frame,
                  text="Period in days after contracting disease before becoming infectious.").grid(row=3,
                                                                                                    column=0,
                                                                                                    columnspan=2,
                                                                                                    sticky="w")

        ttk.Label(disease_frame, text="Recovery Rate:").grid(row=4, column=0, sticky="w")
        self.__params["recovery_rate"] = ttk.Entry(disease_frame)
        self.__params["recovery_rate"].insert(0, "0.6")
        self.__params["recovery_rate"].grid(row=4, column=1)
        ttk.Label(disease_frame,
                  text="Probability of an infected person recovering. Decimal between 0 and 1.").grid(row=5,
                                                                                                      column=0,
                                                                                                      columnspan=2,
                                                                                                      sticky="w")

        ttk.Label(disease_frame, text="Mortality Rate:").grid(row=6, column=0, sticky="w")
        self.__params["mortality_rate"] = ttk.Entry(disease_frame)
        self.__params["mortality_rate"].insert(0, "0.1")
        self.__params["mortality_rate"].grid(row=6, column=1)
        ttk.Label(disease_frame,
                  text="Probability of an infected person dying. Decimal between 0 and 1.").grid(row=7,
                                                                                                 column=0,
                                                                                                 columnspan=2,
                                                                                                 sticky="w")

        # Run and Load Buttons
        ttk.Button(self.__root, text="Run Simulation", command=self.__submit).grid(row=6, column=0, pady=10)
        ttk.Button(self.__root, text="Load Previous Run", command=lambda: self.__load_previous_run(self.__db_name)).grid(row=6,
                                                                                                 column=1,
                                                                                                 pady=10)

    def __update_speed_label(self, value: float) -> None:
        """
        Updates the speed label to the nearest predefined value.

        Args:
            value (float): The current value of the simulation speed.
        """
        # Snap to the nearest predefined value
        closest: float = self.__simulation_speed_values[0] # Initialised to first element
        min_diff: float = abs(closest - float(value)) # Absolute difference between closest and input value

        # Calculate closest value
        for speed in self.__simulation_speed_values:
            diff: float = abs(speed - float(value)) # Calculate difference
            if diff < min_diff:
                min_diff = diff # Find the minimum difference from input value
                closest = speed # Holds value from predefined speed values that is nearest to input value

        self.__simulation_speed.set(closest) # Update simulation speed to the nearest value
        self.__simulation_speed_label.config(text=f"{closest}x") # Update the label text to the nearest value

    def __submit(self) -> None:
        """
        Fetches, validates, and sets simulation parameters. Displays error messages for invalid inputs.

        Raises:
            ValueError: If any input parameters are invalid.
            TypeError: If the input parameters are of incorrect types.
        """
        try:
            # Fetch and validate parameters
            simulation_name: str = self.__is_type(str, self.__params["simulation_name"].get())
            display_size: int = self.__is_type(int, self.__params["display_size"].get())
            num_houses: int = self.__is_type(int, self.__params["num_houses"].get())
            num_offices: int = self.__is_type(int, self.__params["num_offices"].get())
            building_size: int = self.__is_type(int, self.__params["building_size"].get())
            num_people_in_house: int = self.__is_type(int, self.__params["num_people_in_house"].get())
            simulation_speed: float = self.__is_type(float, self.__simulation_speed.get())
            show_drawing: bool = self.__show_drawing.get()
            additional_roads: bool = self.__additional_roads.get()
            infection_rate: float = self.__is_type(float, self.__params["infection_rate"].get())
            incubation_time: float = self.__is_type(float, self.__params["incubation_time"].get())
            recovery_rate: float = self.__is_type(float, self.__params["recovery_rate"].get())
            mortality_rate: float = self.__is_type(float, self.__params["mortality_rate"].get())

            # Validate parameters
            if len(simulation_name) == 0:
                raise ValueError("Please enter a simulation name.")
            if len(simulation_name) > 50:
                raise ValueError("Simulation name is too long. Maximum 50 characters.")
            if display_size <= 0:
                raise ValueError(f"'{display_size}'. Display size must be a positive integer.")
            if display_size > 2160: # 4K display height
                raise ValueError(f"'{display_size}'. Display size too large. Maximum display size is 2160 pixels.")

            # Build raw dict
            raw = {
                "simulation_name": simulation_name,
                "simulation_speed": simulation_speed,
                "display_size": display_size,
                "num_houses": num_houses,
                "num_offices": num_offices,
                "building_size": building_size,
                "num_people_in_house": num_people_in_house,
                "show_drawing": show_drawing,
                "additional_roads": additional_roads,
                "infection_rate": infection_rate,
                "incubation_time": incubation_time,
                "recovery_rate": recovery_rate,
                "mortality_rate": mortality_rate
            }

            try:
                self.__config = Config.from_dict(raw)
            except ConfigError as e:
                messagebox.showerror("Configuration Error", str(e))
                return

            # Warning for large population
            if num_people_in_house * num_houses >= 1000:
                proceed_large_num: bool = messagebox.askokcancel(
                    "Warning",
                    "The population size is large and initialisation may take long.\n"
                    "The simulation may not run smoothly on all systems.\n"
                    "Consider reducing the total number of people, or simulation speed if performance is an issue.\n"
                    "Proceed?",
                    icon='warning',
                    default='cancel'
                )
                if not proceed_large_num:
                    return

            # Warning for large number of buildings
            if num_houses + num_offices >= 500:
                proceed_many_buildings: bool = messagebox.askokcancel(
                    "Warning",
                    "There are a large number of buildings and the road network may take time to generate.\n"
                    "Consider reducing the total number of buildings if this is an issue.\n"
                    "Proceed?",
                    icon='warning',
                    default='cancel'
                )
                if not proceed_many_buildings:
                    return

            # Warning for simulation running forever
            if recovery_rate == 0 and mortality_rate == 0:
                proceed_no_sim_end: bool = messagebox.askokcancel(
                    "Warning",
                    "Both the recovery rate and mortality rate are 0, so the simulation will not end.\n"
                    "Proceed?",
                    icon='warning',
                    default='cancel'
                )
                if not proceed_no_sim_end:
                    return
                
            # Warning for people too small to being visible
            if ((building_size // 10 < 1) or
            (building_size // (2 * (math.ceil(math.sqrt(num_people_in_house)) + 1)) < 1) or
            (building_size // (2 * (math.ceil(math.sqrt((num_people_in_house * num_houses) // num_offices)) + 1)) < 1)):
                proceed_no_sim_end: bool = messagebox.askokcancel(
                    "Warning",
                    "Population size too large and/or building size too small for people to be seen.\n"
                    "Proceed?",
                    icon='warning',
                    default='cancel'
                )
                if not proceed_no_sim_end:
                    return

            self.__root.quit()
            self.__root.destroy()

        # Error handling for different types of errors
        except ValueError as error:
            messagebox.showerror("Input Error", f"Invalid input: {error}")
        except TypeError as error:
            messagebox.showerror("Format Error", f"Invalid input: {error}")
        except Exception as error:
            messagebox.showerror("Error", f"An error occurred. Please check inputs. Error details: {error}")

    def __on_closing(self) -> None:
        """
        Handles the window closing event by setting parameters to None and quitting the main loop.
        """
        self.__params = None
        self.__root.quit()

    def __is_type(self, variable_type: type, value: str) -> type:
        """
        Checks if a value can be converted to the specified type. Raises an error if not.

        Args:
            type (type): The type to check against.
            value (str): The value to check.

        Returns:
            type: The value converted to the specified type.

        Raises:
            TypeError: If the value cannot be converted to the specified type.
        """
        # Allows for generalisation of prompt depending on parameter type
        type_to_english: dict = {
            int: "n integer",
            float: " decimal",
            str: " sequence of characters"
        }

        # Blank field check
        if value == '':
            raise TypeError(f"<blank field>. Please enter a{type_to_english[variable_type]}.")

        # These values could creep through when trying to convert value to intended type
        if value in ['inf', 'Inf', 'infinity', 'Infinity', 'nan', 'Nan', 'NaN']:
            raise TypeError(f"'{value}'. Please enter a{type_to_english[variable_type]}.")

        # Exception handling
        try:
            variable_type(value)
        except Exception:
            raise TypeError(f"'{value}'. Please enter a{type_to_english[variable_type]}.")

        return variable_type(value)

    def __load_previous_run(self, db_name: str) -> None:
        """
        Loads parameters from a previous simulation run from the SQLite database.
        Displays a selection window for the user to choose a previous run.

        Args:
            db_name (str): The name of the database file.
        """
        # If window already exists, bring it to the front
        if self.__load_window is not None and self.__load_window.winfo_exists():
            self.__load_window.lift()
            return

        # Create new window
        self.__load_window = tk.Toplevel(self.__root)
        self.__load_window.title("Select Previous Run")

        # When closed, clear reference
        self.__load_window.protocol("WM_DELETE_WINDOW", self.__close_load_window)

        try:
            with DBHandler(self.__db_name) as db_handler:
                rows: list[tuple] = db_handler.fetch_runs_summary()
        except DBError as e:
            messagebox.showerror("Database Error", str(e))
            return

        if not rows:
            messagebox.showinfo("Load Previous Run", "No previous runs found.")
            self.__close_load_window()
            return

        frame = ttk.Frame(self.__load_window)
        frame.grid(row=0, column=0, padx=10, pady=10)

        tree = ttk.Treeview(
            frame,
            columns=("run_id", "datetime", "simulation_name",
                    "num_houses", "num_offices",
                    "infection_rate", "incubation_time",
                    "recovery_rate", "mortality_rate"),
            show='headings'
        )

        for col in tree["columns"]:
            tree.heading(col, text=col.replace("_", " ").title(), anchor="center")
            tree.column(col, width=150, anchor="center")

        tree.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        for summary in rows:
            tree.insert("", "end", values=(
                summary["run_id"],
                summary["datetime"],
                summary["simulation_name"],
                summary["num_houses"],
                summary["num_offices"],
                summary["infection_rate"],
                summary["incubation_time"],
                summary["recovery_rate"],
                summary["mortality_rate"],
            ))

        ttk.Button(
            self.__load_window,
            text="Load",
            command=lambda: self.__load_selected_run(tree)
        ).grid(row=1, column=0, padx=10, pady=10)

    def __load_selected_run(self, tree: ttk.Treeview) -> None:
        """
        Handles the event when the 'Load' button is clicked.
        Calls __load_run() to load the selected run parameters from the Treeview into the simulation.

        Args:
            tree (ttk.Treeview): The Treeview containing the previous run data.
            selection_window (tk.Toplevel): The window for selecting the previous run.
            db_name (str): The name of the database file.
        """
        selected_item = tree.selection()

        # Handle case where load is clicked but no run is selected
        if not selected_item:
            messagebox.showerror("Selection Error", "No run selected. Please select a run to load.")
            return

        run_id = tree.item(selected_item)["values"][0]
        self.__load_run(run_id)

    def __load_run(self, run_id: int) -> None:
        """
        Loads the parameters of a selected run from the SQLite database into the current simulation settings.

        Args:
            run_id (int): The ID of the selected run.
            selection_window (tk.Toplevel): The window for selecting the previous run.
            db_name (str): The name of the database file.
        """
        try:
            with DBHandler(self.__db_name) as db:
                loaded = db.fetch_run(run_id)
        except DBError as e:
            messagebox.showerror("Database Error", str(e))
            return

        if not loaded:
            messagebox.showerror("Load Error", "Selected run not found.")
            return

        # Fill entry widgets
        for key, value in loaded.items():
            if key in self.__params:
                widget = self.__params[key]
                widget.delete(0, tk.END)
                widget.insert(0, value)

        # Fill non-entry widgets
        self.__simulation_speed.set(loaded["simulation_speed"])
        self.__update_speed_label(loaded["simulation_speed"])
        self.__show_drawing.set(loaded["show_drawing"])
        self.__additional_roads.set(loaded["additional_roads"])

        # Build Config
        self.__config = Config.from_dict(loaded)

        self.__close_load_window()

    def __close_load_window(self):
        if self.__load_window is not None:
            self.__load_window.destroy()
            self.__load_window = None

    def get_config(self) -> Config | None:
        """
        Returns the Config object containing the simulation parameters.

        Returns:
            Config | None: The Config object or None if parameters were not set.
        """
        self.__root.mainloop()
        return self.__config