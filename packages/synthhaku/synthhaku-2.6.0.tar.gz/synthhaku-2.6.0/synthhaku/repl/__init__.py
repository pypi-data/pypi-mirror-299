# -*- coding: utf-8 -*-

"""
synthhaku.repl
~~~~~~~~~~~~

Repl-related operations and tools for Jishaku.

:copyright: (c) 2021 Devon (Gorialis) R
:license: MIT, see LICENSE for more details.

"""

# pylint: disable=wildcard-import
from synthhaku.repl.compilation import *  # noqa: F401
from synthhaku.repl.disassembly import create_tree, disassemble, get_adaptive_spans  # type: ignore  # noqa: F401
from synthhaku.repl.inspections import all_inspections  # type: ignore  # noqa: F401
from synthhaku.repl.repl_builtins import get_var_dict_from_ctx  # type: ignore  # noqa: F401
from synthhaku.repl.scope import *  # noqa: F401
