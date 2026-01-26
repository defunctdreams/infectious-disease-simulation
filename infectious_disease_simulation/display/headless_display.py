import pygame

class Display:
    """
    Null display for headless / no-render mode.
    Provides the same API as real Display, but does nothing.
    """

    def __init__(self, width: int, height: int, caption: str) -> None:
        self.__width = width
        self.__height = height
        self.__caption = caption
        # Dummy surface so pygame.draw.* still works if called
        self.__screen = pygame.Surface((width, height))

    def get_caption(self) -> str:
        return self.__caption

    def set_caption(self) -> None:
        pass

    def fill(self, colour: tuple[int, int, int]) -> None:
        pass

    def update(self) -> None:
        pass

    def get_width(self) -> int:
        return self.__width

    def get_height(self) -> int:
        return self.__height

    def get_screen(self) -> pygame.Surface:
        return self.__screen

    def set_display_icon(self, filepath: str) -> None:
        pass
