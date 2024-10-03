from setuptools import setup
from setuptools.command.install import install
import os
import platform
import urllib.request
import json
import zipfile

__versionList__ = [1, 0, 0, 0]

# Stable, Alpha, Beta
__versionData__ = {"version": f"{__versionList__[0]}.{__versionList__[1]}", "build": f"{__versionList__[2]}{f'.{__versionList__[3]}' if __versionList__[3] else ''}", "phase": "Beta"}

__version__ = f"{__versionData__['version']}.{__versionData__['build']}"

class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        install.run(self)
        self.download_sdl_dlls()

    def download_sdl_dlls(self):
        system = platform.system().lower()

        with urllib.request.urlopen(f"https://deps.libmge.org/?version={__version__}&release={__versionData__['phase']}&os={system}") as response:
            data = response.read().decode('utf-8')

        # Converte os dados lidos (em formato JSON) para um dicionário
        data = json.loads(data)

        if 'error' in data:
            pass
        else:
            # Faz o download das DLLs
            print(f"Baixando SDL2 de {data['download']}")
            urllib.request.urlretrieve(data['download'], "sdl.zip")

            # Extrai os arquivos (somente um exemplo, ajuste conforme necessário)
            with zipfile.ZipFile("sdl.zip", 'r') as zip_ref:
                zip_ref.extractall("./libs/")

            # Faça a movimentação das DLLs conforme necessário
            dlls = ("SDL2.dll", "SDL2_gfx.dll", "SDL2_image.dll", "SDL2_mixer.dll", "SDL2_ttf.dll")
            for dll in dlls:
                os.rename(f"./libs/{dll}", f"./{dll}")

setup(
    name="MGE",  # Nome do projeto
    version="1.0.0.2-beta",  # Versão Beta 1.0.0
    license='MIT License',
    description="LibMGE is a graphical user interface library for developing 2D programs and games.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Lucas Guimarães",  # Nome do autor
    author_email="commercial@lucasguimaraes.pro",  # Email do autor
    url="https://libmge.org/",  # Site do projeto
    project_urls={
        "Source": "https://github.com/MonumentalGames/LibMGE",  # Link para o GitHub
        "Documentation": "https://docs.libmge.org/",  # link to package document
        "Author Website": "https://lucasguimaraes.pro/"  # Site pessoal do autor
    },
    python_requires=">=3.5",  # Suporte para Python >= 3.5
    packages=[
          "MGE",
          "MGE/_sdl",
          "MGE/_InputsEmulator"
    ],
    install_requires=[
        "numpy"  # Dependência necessária (numpy)
    ],
    classifiers=[
        "Development Status :: 4 - Beta",  # Indica que é uma versão beta
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "License :: OSI Approved :: MIT License",  # Licença do projeto (ajuste conforme sua escolha)
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: Microsoft :: Windows",  # Suporte apenas para Windows
    ],
    cmdclass={
        'install': PostInstallCommand,
    },
    keywords="2D development, graphical interface, games",  # Palavras-chave relacionadas ao projeto
)
