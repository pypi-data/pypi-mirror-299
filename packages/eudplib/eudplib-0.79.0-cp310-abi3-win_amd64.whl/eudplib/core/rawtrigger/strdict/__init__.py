# Copyright 2022 by Armoha.
# All rights reserved.
# This file is part of EUD python library (eudplib),
# and is released under "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.

from .flingy import DefFlingyDict
from .icon import DefIconDict
from .image import DefImageDict
from .iscript import DefIscriptDict
from .portrait import DefPortraitDict
from .sfxdata import DefSfxDataDict
from .sprite import DefSpriteDict
from .stattxt import DefRankDict, DefStatTextDict
from .tech import DefTechDict
from .trg import (
    DefAIScriptDict,
    DefLocationDict,
    DefSwitchDict,
    DefUnitDict,
)
from .unitorder import DefUnitOrderDict
from .upgrade import DefUpgradeDict
from .weapon import DefWeaponDict

__all__ = [
    "DefFlingyDict",
    "DefIconDict",
    "DefImageDict",
    "DefIscriptDict",
    "DefPortraitDict",
    "DefSfxDataDict",
    "DefSpriteDict",
    "DefRankDict",
    "DefStatTextDict",
    "DefTechDict",
    "DefAIScriptDict",
    "DefLocationDict",
    "DefSwitchDict",
    "DefUnitDict",
    "DefUnitOrderDict",
    "DefUpgradeDict",
    "DefWeaponDict",
]
