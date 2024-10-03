"""
Plover entry point extension module for Plover Run AppleScript.

    - https://plover.readthedocs.io/en/latest/plugin-dev/extensions.html
    - https://plover.readthedocs.io/en/latest/plugin-dev/commands.html
"""

from pathlib import Path
from typing import Any

from plover.engine import StenoEngine
from plover.machine.base import STATE_RUNNING
from plover.oslayer.config import CONFIG_DIR
from plover.registry import registry

from PyXA import AppleScript

from . import (
    applescript,
    config,
    path
)


_CONFIG_FILE: Path = Path(CONFIG_DIR) / config.CONFIG_BASENAME

class RunAppleScript:
    """
    Extension class that also registers a command plugin.
    The command deals with loading, storing, and running external AppleScript
    files.
    """

    _applescripts: dict[str, Any]
    _engine: StenoEngine

    def __init__(self, engine: StenoEngine) -> None:
        self._engine = engine

    def start(self) -> None:
        """
        Sets up the command plugin and steno engine hooks
        """
        self._applescripts = config.load(_CONFIG_FILE)
        registry.register_plugin(
            "command",
            "APPLESCRIPT",
            self._run_applescript
        )
        self._engine.hook_connect(
            "machine_state_changed",
            self._machine_state_changed
        )

    def stop(self) -> None:
        """
        Tears down the steno engine hooks
        """
        self._engine.hook_disconnect(
            "machine_state_changed",
            self._machine_state_changed
        )

    def _run_applescript(self, _engine: StenoEngine, argument: str) -> Any:
        """
        Loads an external AppleScript and stores it in memory for faster
        execution on subsequent calls.
        """
        if not argument:
            raise ValueError("No AppleScript code/filepath provided")

        if not argument.endswith(applescript.FILE_EXTENSION):
            return applescript.run_code(argument)

        script: AppleScript
        try:
            script = self._applescripts[argument]
        except KeyError:
            filepath: str = path.expand(argument)
            script = applescript.load(filepath)
            self._applescripts[argument] = script
            config.save(_CONFIG_FILE, sorted(self._applescripts.keys()))

        return applescript.run_script(script)

    def _machine_state_changed(
        self,
        _machine_type: str,
        machine_state: str
    ) -> None:
        """
        This hook will be called when when the Plover UI "Reconnect" button is
        pressed. Resetting the `_applescripts` dictionary allows for changes
        made to external AppleScripts to be re-read in.
        """
        if machine_state == STATE_RUNNING:
            self._applescripts = config.load(_CONFIG_FILE)
