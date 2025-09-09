"""
Defines the PlotGraph class to plot and update a graph for disease simulation data.

Imports:
    matplotlib.pyplot

Classes:
    PlotGraph
"""

import matplotlib.pyplot as plt

class PlotGraph:
    """
    A class to plot and update a graph for disease simulation data.

    Attributes:
        __figure (plt.Figure): The matplotlib figure object.
        __axis (plt.Axes): The axes of the plot.
        __caption (str): The caption for the graph window.
        __fps (int): The frames per second for updating the graph.
        __hours (list[int]): The list of hours passed in the simulation.
        __susceptible (list[int]): The list of susceptible counts over time.
        __exposed (list[int]): The list of exposed counts over time.
        __infected (list[int]): The list of infected counts over time.
        __recovered (list[int]): The list of recovered counts over time.
        __deceased (list[int]): The list of deceased counts over time.
        __sus_line (plt.Line2D): The line object for susceptible counts.
        __exp_line (plt.Line2D): The line object for exposed counts.
        __inf_line (plt.Line2D): The line object for infected counts.
        __rec_line (plt.Line2D): The line object for recovered counts.
        __dec_line (plt.Line2D): The line object for deceased counts.
        __sus_text (plt.Text): Text annotation for the most recent susceptible count.
        __exp_text (plt.Text): Text annotation for the most recent exposed count.
        __inf_text (plt.Text): Text annotation for the most recent infected count.
        __rec_text (plt.Text): Text annotation for the most recent recovered count.
        __dec_text (plt.Text): Text annotation for the most recent deceased count.
    """
    def __init__(self, caption: str, fps: int) -> None:
        """
        Initialises the Graph class with the given parameters.

        Args:
            caption (str): The caption for the graph window.
            seconds_per_hour (int): The number of seconds per simulation hour.
            fps (int): The frames per second for updating the graph.
        """
        plt.ion() # Turn on interactive mode
        self.__figure, self.__axis = plt.subplots()
        self.__caption: str = caption
        self.__fps: int = fps

        # Initialise lists
        self.__hours: list[int] = []
        self.__susceptible: list[int] = []
        self.__exposed: list[int] = []
        self.__infected: list[int] = []
        self.__recovered: list[int] = []
        self.__deceased: list[int] = []

        # Initialise lines
        self.__sus_line, = self.__axis.plot([], [], label='Susceptible (S)', color='green')
        self.__exp_line, = self.__axis.plot([], [], label='Exposed (E)', color='orange')
        self.__inf_line, = self.__axis.plot([], [], label='Infected (I)', color='red')
        self.__rec_line, = self.__axis.plot([], [], label='Recovered (R)', color='purple')
        self.__dec_line, = self.__axis.plot([], [], label='Deceased (D)', color='black')

        # Set graph labels and properties
        self.__figure.canvas.manager.set_window_title(f"{self.__caption} - Graph")
        self.__axis.set_xlabel("Hour")
        self.__axis.set_ylabel("Population")
        self.__axis.set_title(f"{self.__caption} - Graph")
        self.__axis.legend()

        # Initialize text annotations for the most recent values
        self.__sus_text = self.__axis.text(0.02, 0.95, '', transform=self.__axis.transAxes, color='green')
        self.__exp_text = self.__axis.text(0.02, 0.90, '', transform=self.__axis.transAxes, color='orange')
        self.__inf_text = self.__axis.text(0.02, 0.85, '', transform=self.__axis.transAxes, color='red')
        self.__rec_text = self.__axis.text(0.02, 0.80, '', transform=self.__axis.transAxes, color='purple')
        self.__dec_text = self.__axis.text(0.02, 0.75, '', transform=self.__axis.transAxes, color='black')

        plt.show()

    def update(self, day: int, hour: int, counts: dict[str, int]) -> None:
        """
        Updates the graph with new data for the current day and hour.

        Args:
            day (int): The current day in the simulation.
            hour (int): The current hour in the simulation.
            counts (dict[str, int]): A dictionary containing the counts for each category (S, E, I, R, D).
        """
        # Add values to list
        self.__hours.append(((day - 1) * 24) + hour)
        self.__susceptible.append(counts['S'])
        self.__exposed.append(counts['E'])
        self.__infected.append(counts['I'])
        self.__recovered.append(counts['R'])
        self.__deceased.append(counts['D'])

        # Set data based on the list values
        self.__sus_line.set_xdata(self.__hours)
        self.__sus_line.set_ydata(self.__susceptible)

        self.__exp_line.set_xdata(self.__hours)
        self.__exp_line.set_ydata(self.__exposed)

        self.__inf_line.set_xdata(self.__hours)
        self.__inf_line.set_ydata(self.__infected)

        self.__rec_line.set_xdata(self.__hours)
        self.__rec_line.set_ydata(self.__recovered)

        self.__dec_line.set_xdata(self.__hours)
        self.__dec_line.set_ydata(self.__deceased)

        self.__axis.relim()
        self.__axis.autoscale_view()

        # Update the text annotations with the most recent values
        self.__sus_text.set_text(f"Susceptible: {self.__susceptible[-1]}")
        self.__exp_text.set_text(f"Exposed: {self.__exposed[-1]}")
        self.__inf_text.set_text(f"Infected: {self.__infected[-1]}")
        self.__rec_text.set_text(f"Recovered: {self.__recovered[-1]}")
        self.__dec_text.set_text(f"Deceased: {self.__deceased[-1]}")

        plt.pause(1 / self.__fps)
