"""
Plover Steno Engine Hooks Logger - A Plover GUI Tool to log out the contents of
steno engine hooks using Qt signals.
"""

from plover.engine import StenoEngine
from plover.gui_qt.tool import Tool

from .steno_engine_hooks import Logger


# REF: https://stackoverflow.com/a/28727066/567863
class _MetaClass(type(Logger), type(Tool)): # type: ignore
    """
    Metaclass to prevent the following error:
    `TypeError: metaclass conflict: the metaclass of a derived class must be a
    (non-strict) subclass of the metaclasses of all its bases`
    """

class StenoEngineHooksLoggerGUITool(Logger, Tool, metaclass=_MetaClass): # type: ignore
    """
    Plover entry point GUI Tool class to log the contents of steno engine
    hooks.
    """

    TITLE: str = "Steno Engine\nHooks Logger"
    ICON: str = ""
    ROLE: str = "Steno Engine Hooks Logger"

    def __init__(self, engine: StenoEngine) -> None:
        Logger.__init__(self, entry_point="GUI")
        Tool.__init__(self, engine)

        for hook in self._HOOKS:
            engine.signal_connect(hook, getattr(self, f"_{hook}"))
