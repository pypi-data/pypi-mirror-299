from setuptools import setup
import sys
import platform
import urllib.request
import json
import zipfile

def install():
    from MGE.Version import __version__, __versionData__, __versionList__
    from MGE.Log import LogCritical, LogError, Log

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

        Log("Successfully installed")

        #dlls = ("SDL2.dll", "SDL2_gfx.dll", "SDL2_image.dll", "SDL2_mixer.dll", "SDL2_ttf.dll")
        #for dll in dlls:
        #    os.rename(f"./libs/{dll}", f"./MGE/{dll}")

def main():
    from MGE.Version import __version__, __versionData__, __versionList__
    from MGE.Log import LogCritical, LogError

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

    LogError()

setup(
    name="MGE",
    version="1.0.0.5-beta",
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
    entry_points={
        'console_scripts': [
            'MGE=MGE.setup:main',
            'mge=MGE.setup:main',
        ],
    },
    keywords="2D development, graphical interface, games",
)
