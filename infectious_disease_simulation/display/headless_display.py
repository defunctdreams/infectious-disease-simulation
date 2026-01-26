import pygame
from .base_display import BaseDisplay

class HeadlessDisplay(BaseDisplay):
    """
    Null display for headless / no-render mode.
    Provides the same API as real Display, but does nothing.
    """

    def __init__(self, width: int, height: int, caption: str) -> None:
        super().__init__(width, height, caption)
        # Dummy surface so pygame.draw.* still works if called
        self.__screen = pygame.Surface((width, height))

    def is_headless(self) -> bool:
        return True

    def set_caption(self) -> None:
        pass

    def fill(self, colour: tuple[int, int, int]) -> None:
        pass

    def update(self) -> None:
        pass

    def get_screen(self) -> pygame.Surface:
        return self.__screen

    def set_display_icon(self, filepath: str) -> None:
        pass
