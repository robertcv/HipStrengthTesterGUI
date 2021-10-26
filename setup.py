import setuptools

# get long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hst",
    version="2.0.0",
    author="Robert Cvitkovič",
    author_email="robert.cvitkovic@gmail.com",
    description="Software for the DIY hip strength tester.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/robertcv/HipStrengthTesterGUI",
    classifiers=[
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: Microsoft :: Windows"
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Terminals :: Serial",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    entry_points={"console_scripts": ["hst=hst.__main__:main"]},
)
