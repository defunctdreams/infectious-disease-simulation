"""
Defines the Disease class to model the spread, recovery, and mortality of an infectious disease.

Imports:
    random

Classes:
    Disease
"""

import random

class Disease:
    """
    A class to model the spread, recovery, and mortality of an infectious disease.

    Attributes:
        __seconds_per_hour (float): The number of seconds per simulation hour.
        __infection_rate (float): The rate of infection per hour.
        __incubation_time (float): The incubation time of the disease in real seconds.
        __recovery_rate (float): The rate of recovery per hour.
        __mortality_rate (float): The rate of mortality per hour.
    """
    def __init__(self, infection_rate: float, incubation_time: float,
                 recovery_rate: float, mortality_rate: float,
                 seconds_per_hour: float) -> None:
        """
        Initialises the Disease class with the given parameters.

        Args:
            infection_rate (float): The rate of infection per day.
            incubation_time (float): The incubation time in days.
            recovery_rate (float): The rate of recovery per day.
            mortality_rate (float): The rate of mortality per day.
            seconds_per_hour (float): The number of seconds per simulation hour.
        """
        self.__seconds_per_hour: float = seconds_per_hour
        self.__infection_rate: float = infection_rate / 24
        self.__incubation_time: float = incubation_time * 24 * self.__seconds_per_hour
        self.__recovery_rate: float = recovery_rate / 24
        self.__mortality_rate: float = mortality_rate / 24

    def infect(self) -> bool:
        """
        Simulates whether an infection occurs based on the infection rate.

        Returns:
            bool: True if infection occurs, False otherwise.
        """
        return random.randint(0, 1000) < self.__infection_rate * 1000

    def recover(self) -> bool:
        """
        Simulates whether recovery occurs based on the recovery rate.

        Returns:
            bool: True if recovery occurs, False otherwise.
        """
        return random.randint(0, 1000) < self.__recovery_rate * 1000

    def die(self) -> bool:
        """
        Simulates whether death occurs based on the mortality rate.

        Returns:
            bool: True if death occurs, False otherwise.
        """
        return random.randint(0, 1000) < self.__mortality_rate * 1000

    def get_incubation_time(self) -> float:
        """
        Gets the incubation time of the disease.

        Returns:
            float: The incubation time of the disease in seconds.
        """
        return self.__incubation_time
