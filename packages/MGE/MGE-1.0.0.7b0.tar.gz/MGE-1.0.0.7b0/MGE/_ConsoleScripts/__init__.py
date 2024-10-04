from typing import NoReturn
import os
import sys
import tempfile
import platform
import urllib.request
import json
import zipfile

__versionList__ = [1, 0, 0, 0]

# Stable, Alpha, Beta
__versionData__ = {"version": f"{__versionList__[0]}.{__versionList__[1]}", "build": f"{__versionList__[2]}{f'.{__versionList__[3]}' if __versionList__[3] else ''}", "phase": "Beta"}

__version__ = f"{__versionData__['version']}.{__versionData__['build']}"

class _ConsoleColors:
    Reset = "\033[0m"
    Gray = "\033[90m"
    Red = "\033[91m"
    Green = "\033[92m"
    Yellow = "\033[93m"
    Blue = "\033[94m"
    Purple = "\033[95m"
    Cyan = "\033[96m"
    White = "\033[97m"

def Log(msg=""):
    print(f"{_ConsoleColors.Gray}{msg}{_ConsoleColors.Reset}")

def LogDebug(msg=""):
    print(f"{_ConsoleColors.Yellow}Debug{_ConsoleColors.Reset}: {msg}")

def LogInfo(msg=""):
    print(f"{_ConsoleColors.Green}Info{_ConsoleColors.Reset}: {_ConsoleColors.Gray}{msg}{_ConsoleColors.Reset}")

def LogWarn(msg=""):
    print(f"{_ConsoleColors.Yellow}Warning{_ConsoleColors.Reset}: {msg}")

def LogError(msg=""):
    print(f"{_ConsoleColors.Red}Error{_ConsoleColors.Reset}: {msg}")

def LogCritical(msg="", long_msg="", exit_code=1) -> NoReturn:
    print(f"{_ConsoleColors.Red}Critical Error{_ConsoleColors.Reset}: {msg}")
    if long_msg:
        Log(long_msg)
    raise SystemExit(exit_code)

def install():
    print("Checking compatibility")

    system = platform.system().lower()

    with urllib.request.urlopen(f"https://deps.libmge.org/?version={__version__}&release={__versionData__['phase']}&os={system}") as response:
        data = response.read().decode('utf-8')

    data = json.loads(data)

    if 'error' in data:
        LogCritical(data["error"]["title"], data["error"]["message"])
    else:
        print(f"Downloading SDL2 from {data['download']}")

        # Definir o caminho temporário do arquivo zip
        temp_zip_path = os.path.join(tempfile.gettempdir(), 'sdl.zip')

        urllib.request.urlretrieve(data['download'], temp_zip_path)

        print(f"Extracting SDL2 files")

        with zipfile.ZipFile(temp_zip_path, 'r') as zip_ref:
            zip_ref.extractall(os.path.abspath(os.path.dirname(__file__)))

        Log("Successfully installed")

def main():
    if sys.argv[1].lower() == "version":
        print(f"{'MGE' if __versionData__['phase'] == 'Stable' else __versionData__['phase'] + '-MGE'} {__version__}")
    elif sys.argv[1].lower() == "deps":
        if len(sys.argv) >= 2:
            if sys.argv[2].lower() == "install":
                install()
            elif sys.argv[2].lower() == "update":
                pass
            elif sys.argv[2].lower() == "versions":
                pass

    #LogError()
