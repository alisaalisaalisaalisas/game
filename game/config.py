from dataclasses import dataclass
from typing import List, Optional, Optional
import json
import os


CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")


@dataclass
class VideoConfig:
    width: int = 1400
    height: int = 800
    fullscreen: bool = False


@dataclass
class AudioConfig:
    master: float = 1.0
    music: float = 1.0
    sfx: float = 1.0


@dataclass
class UIConfig:
    debug_overlay: bool = False
    animations: bool = False
    language: str = "ru"


@dataclass
class InputConfig:
    jump: str = "SPACE"
    left: List[str] = None
    right: List[str] = None
    escape_to_menu: str = "ESCAPE"


@dataclass
class GameConfig:
    video: VideoConfig
    audio: AudioConfig
    input: InputConfig
    ui: UIConfig


def load_config() -> GameConfig:
    """Загружает конфигурацию игры из config.json или возвращает значения по умолчанию.

    Значения по умолчанию подобраны так, чтобы полностью повторять
    текущее поведение (1400x800, окно, громкости = 1.0 и т.п.).
    """
    if not os.path.exists(CONFIG_PATH):
        return GameConfig(
            video=VideoConfig(),
            audio=AudioConfig(),
            input=InputConfig(left=["LEFT", "A"], right=["RIGHT", "D"]),
            ui=UIConfig(),
        )

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        raw = json.load(f)

    v = raw.get("video", {})
    a = raw.get("audio", {})
    i = raw.get("input", {})
    u = raw.get("ui", {})

    return GameConfig(
        video=VideoConfig(
            width=v.get("width", 1400),
            height=v.get("height", 800),
            fullscreen=v.get("fullscreen", False),
        ),
        audio=AudioConfig(
            master=a.get("master", 1.0),
            music=a.get("music", 1.0),
            sfx=a.get("sfx", 1.0),
        ),
        input=InputConfig(
            jump=i.get("jump", "SPACE"),
            left=i.get("left", ["LEFT", "A"]),
            right=i.get("right", ["RIGHT", "D"]),
            escape_to_menu=i.get("escape_to_menu", "ESCAPE"),
        ),
        ui=UIConfig(
            debug_overlay=u.get("debug_overlay", False),
            animations=u.get("animations", False),
            language=u.get("language", "ru"),
        ),
    )
