# -*- coding: utf-8 -*-

"""
synthhaku
~~~~~~~

A discord.py extension including useful tools for bot development and debugging.

:copyright: (c) 2021 Devon (Gorialis) R
:license: MIT, see LICENSE for more details.

"""

# pylint: disable=wildcard-import
from synthhaku.cog import *  # noqa: F401
from synthhaku.features.baseclass import Feature  # noqa: F401
from synthhaku.flags import Flags  # noqa: F401
from synthhaku.meta import *  # noqa: F401

__all__ = ("Feature", "Flags", "setup")
