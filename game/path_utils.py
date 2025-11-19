import os
import sys


def resource_path(*parts: str) -> str:
    """Возвращает абсолютный путь к ресурсу, совместимый с PyInstaller.

    В режиме разработки использует корень проекта, а в собранном
    бинарнике PyInstaller — временную директорию _MEIPASS.
    """
    if hasattr(sys, "_MEIPASS"):
        base = getattr(sys, "_MEIPASS")  # type: ignore[attr-defined]
    else:
        # ../ от папки game -> корень проекта
        base = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(base, *parts)
