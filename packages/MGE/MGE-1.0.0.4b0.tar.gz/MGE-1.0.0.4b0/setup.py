from setuptools import setup
from setuptools.command.install import install
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

def LogCritical(msg="", long_msg="", exit_code=1):
    print(f"{_ConsoleColors.Red}Critical Error{_ConsoleColors.Reset}: {msg}")
    if long_msg:
        Log(long_msg)
    raise SystemExit(exit_code)

class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        install.run(self)
        system = platform.system().lower()

        with urllib.request.urlopen(f"https://deps.libmge.org/?version={__version__}&release={__versionData__['phase']}&os={system}") as response:
            data = response.read().decode('utf-8')

        data = json.loads(data)

        if 'error' in data:
            LogCritical(data["error"]["title"], data["error"]["message"])
        else:
            print(f"Downloading SDL2 from {data['download']}")
            urllib.request.urlretrieve(data['download'], "sdl.zip")

            with zipfile.ZipFile("sdl.zip", 'r') as zip_ref:
                zip_ref.extractall("./MGE/")

            #dlls = ("SDL2.dll", "SDL2_gfx.dll", "SDL2_image.dll", "SDL2_mixer.dll", "SDL2_ttf.dll")
            #for dll in dlls:
            #    os.rename(f"./libs/{dll}", f"./MGE/{dll}")

setup(
    name="MGE",
    version="1.0.0.4-beta",
    license='MIT License',
    description="LibMGE is a graphical user interface library for developing 2D programs and games.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Lucas Guimarães",
    author_email="commercial@lucasguimaraes.pro",
    url="https://libmge.org/",
    project_urls={
        "Source": "https://github.com/MonumentalGames/LibMGE",
        "Documentation": "https://docs.libmge.org/",
        "Author Website": "https://lucasguimaraes.pro/"
    },
    python_requires=">=3.5",
    packages=[
          "MGE",
          "MGE/_sdl",
          "MGE/_InputsEmulator"
    ],
    install_requires=[
        "numpy"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: Microsoft :: Windows",
    ],
    cmdclass={
        'install': PostInstallCommand,
    },
    #entry_points={
    #    'console_scripts': [
    #        'mge-sdl-update=MGE.setup:post_install',  # Comando executável via terminal
    #    ],
    #},
    keywords="2D development, graphical interface, games",
)
