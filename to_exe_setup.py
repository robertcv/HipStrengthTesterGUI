import sys
from cx_Freeze import setup, Executable

build_options = {
    "build_exe": {
        "packages": ["serial"],
        "excludes": ["tkinter"]
    }
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [
    Executable('hst.py', base=base)
]

setup(
    name="HST",
    version="0.1",
    options=build_options,
    executables=executables
)