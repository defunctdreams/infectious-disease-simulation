"""
Defines the Display class, which manages display properties and pygame modules for handling display.

Imports:
    pygame

Classes:
    Display
"""

import pygame
from .base_display import BaseDisplay

class PygameDisplay(BaseDisplay):
    """
    A class which holds display properties, and pygame modules which manage the display window.

    Attributes:
        __width (int): The width of the display.
        __height (int): The height of the display.
        __caption (str): The display window's caption.
        __screen (pygame.Surface): The pygame display surface, using the display width and height.
    """
    def __init__(self, width: int, height: int, caption: str) -> None:
        """
        Initialises the display with given parameters.

        Args:
            width (int): The width of the display.
            height (int): The height of the display.
            caption (str): The display window's caption.
        """
        super().__init__(width, height, caption)
        self.__screen: pygame.Surface = pygame.display.set_mode((self._width, self._height))
        pygame.font.init()
        self.__font: pygame.font.Font = pygame.font.SysFont('Arial Bold', 25)

    def is_headless(self) -> bool:
        return False

    def set_caption(self) -> None:
        """
        Sets the caption of the display window.
        """
        pygame.display.set_caption(self._caption)

    def fill(self, colour: tuple[int, int, int]) -> None:
        """
        Fills the display screen with the given colour.

        Args:
            colour (tuple[int, int, int]): The colour to fill the display screen with.
        """
        self.__screen.fill(colour)

    def update(self) -> None:
        """
        Updates the display screen.
        """
        pygame.display.update()

    def set_display_icon(self, filepath: str) -> None:
        """
        Tries to set the display icon. Does nothing if the file does not exist.
        
        Args:
            filepath (str): Path to the icon image file.
        """
        try:
            icon: pygame.Surface = pygame.image.load(filepath)
            pygame.display.set_icon(icon)
        except:
            pass
    
    def get_screen(self) -> pygame.Surface:
        return self.__screen

    def draw_text(self, text: str, pos=(10, 10), colour=(0,0,0)) -> None:
        if not self.__font:
            return
        surface = self.__font.render(text, True, colour)
        self.__screen.blit(surface, pos)
