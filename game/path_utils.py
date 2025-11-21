import os
import sys


def resource_path(*parts: str) -> str:
    """Get the absolute path to a resource, compatible with PyInstaller.

    This function works in both development and PyInstaller-bundled modes:
    - In development: Uses the project root directory
    - In PyInstaller bundle: Uses the temporary _MEIPASS directory

    Args:
        *parts: Path components to join (e.g., "game", "assets", "player", "sprite.png")

    Returns:
        str: Absolute path to the resource that works in both modes

    Example:
        >>> resource_path("game", "assets", "player", "alienPink_stand.png")
        # Development: "C:/Users/User/Desktop/игра/game/assets/player/alienPink_stand.png"
        # PyInstaller: "C:/Users/User/AppData/Local/Temp/_MEI12345/game/assets/player/alienPink_stand.png"
    """
    if hasattr(sys, "_MEIPASS"):
        # PyInstaller mode: use the temporary extraction directory
        base = getattr(sys, "_MEIPASS")  # type: ignore[attr-defined]
    else:
        # Development mode: calculate project root (parent of 'game' directory)
        base = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(base, *parts)
