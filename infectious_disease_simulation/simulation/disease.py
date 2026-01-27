"""
Defines the Disease class to model the spread, recovery, and mortality of an infectious disease.

Imports:
    random

Classes:
    Disease
"""

import random
import math

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
                 seconds_per_hour: float, rng: random.Random | None = None) -> None:
        """
        Initialises the Disease class with the given parameters.

        Args:
            infection_rate (float): The rate of infection per day.
            incubation_time (float): The incubation time in days.
            recovery_rate (float): The rate of recovery per day.
            mortality_rate (float): The rate of mortality per day.
            seconds_per_hour (float): The number of seconds per simulation hour.
        """
        self.__infection_rate: float = float(infection_rate)
        self.__incubation_time: float = float(incubation_time)
        self.__recovery_rate: float = float(recovery_rate)
        self.__mortality_rate: float = float(mortality_rate)
        self.__seconds_per_hour: float = float(seconds_per_hour)
        self.__rng: random.Random = rng or random.Random()

        self.__lambda_infect = self.__daily_to_lambda(self.__infection_rate)
        self.__lambda_recover = self.__daily_to_lambda(self.__recovery_rate)
        self.__lambda_die = self.__daily_to_lambda(self.__mortality_rate)
        self.__incubation_time = self.__incubation_time * 24 * self.__seconds_per_hour

    def __daily_to_lambda(self, prob):
        """
        Convert daily probability p_day to hazard (lambda) per real second:
        p_day = 1 - exp(-lambda * 24 * seconds_per_hour) => lambda = -ln(1 - p_day) / (24 * seconds_per_hour)
        """
        if prob <= 0:
            return 0.0
        if prob >= 1:
            return float('inf')
        # Avoid division by zero
        denominator: float = 24 * self.__seconds_per_hour
        return -math.log(1.0 - prob) / denominator

    def __happens(self, lambda_rate: float, delta_time: float) -> bool:
        # lambda_rate is hazard per real second
        if lambda_rate == 0.0:
            return False
        if math.isinf(lambda_rate):
            return delta_time > 0.0
        prob: float = 1.0 - math.exp(-lambda_rate * delta_time)
        return self.__rng.random() < prob

    def infect(self, delta_time: float) -> bool:
        """
        Simulates whether an infection occurs based on the infection rate.

        Returns:
            bool: True if infection occurs, False otherwise.
        """
        return self.__happens(self.__lambda_infect, delta_time)

    def recover(self, delta_time) -> bool:
        """
        Simulates whether recovery occurs based on the recovery rate.

        Returns:
            bool: True if recovery occurs, False otherwise.
        """
        return self.__happens(self.__lambda_recover, delta_time)

    def die(self, delta_time) -> bool:
        """
        Simulates whether death occurs based on the mortality rate.

        Returns:
            bool: True if death occurs, False otherwise.
        """
        return self.__happens(self.__lambda_die, delta_time)

    def get_incubation_time(self) -> float:
        """
        Gets the incubation time of the disease.

        Returns:
            float: The incubation time of the disease in seconds.
        """
        return self.__incubation_time
