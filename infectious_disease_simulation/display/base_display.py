from abc import ABC, abstractmethod
import pygame

class BaseDisplay(ABC):
    """
    Abstract base class for display
    """
    def __init__(self, width: int, height: int, caption: str) -> None:
        self._width = width
        self._height = height
        self._caption = caption

    @abstractmethod
    def is_headless(self) -> bool:
        pass

    @abstractmethod
    def get_screen(self) -> pygame.Surface:
        pass

    @abstractmethod
    def update(self) -> None:
        pass

    @abstractmethod
    def fill(self, colour: tuple[int, int, int]) -> None:
        pass

    @abstractmethod
    def set_caption(self, caption: str) -> None:
        pass

    @abstractmethod
    def set_display_icon(self, filepath: str) -> None:
        pass

    def get_width(self) -> int:
        return self._width
    
    def get_height(self) -> int:
        return self._height
    
    def get_caption(self) -> str:
        return self._caption