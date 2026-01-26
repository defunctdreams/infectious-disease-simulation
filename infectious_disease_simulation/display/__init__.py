# display/__init__.py
from .pygame_display import Display as PygameDisplay
from .headless_display import Display as HeadlessDisplay

def Display(width: int, height: int, caption: str, headless: bool):
    if headless:
        return HeadlessDisplay(width, height, caption)
    return PygameDisplay(width, height, caption)
