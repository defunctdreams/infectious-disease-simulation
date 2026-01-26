# display/__init__.py
def Display(width: int, height: int, caption: str, headless: bool):
    if headless:
        from .headless_display import HeadlessDisplay
        return HeadlessDisplay(width, height, caption)
    else:
        from .pygame_display import PygameDisplay
        return PygameDisplay(width, height, caption)
