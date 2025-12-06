from collections import namedtuple
from typing import TypeAlias

Tile = namedtuple("Tile", ["position", "cell"])
Tiles: TypeAlias = list[Tile]
