"""
Script - A module to wrap around PyXA's AppleScript functionality. Mostly
exists to provide appropriate error handling and messages for the plugin.
"""

from typing import Any

from PyXA import AppleScript


def load(filepath: str) -> AppleScript:
    """
    Wrapper around AppleScript.load(path)
    """
    try:
        script: AppleScript = AppleScript.load(filepath)
    except AttributeError as exc:
        raise ValueError(f"Unable to load file from: {filepath}") from exc

    return script

def run_code(code: str) -> Any:
    """
    Creates an AppleScript from `code` then runs it.
    """
    return run_script(AppleScript(code))

# NOTE: PyXA defines AppleScript.run as returning Any
# REF: https://github.com/SKaplanOfficial/PyXA/blob/main/PyXA/XABase.py#L2041
def run_script(script: AppleScript) -> Any:
    """
    Wrapper around AppleScript.run(self)
    """
    result = script.run()

    if not result:
        raise ValueError("AppleScript code errored during execution")

    return result
