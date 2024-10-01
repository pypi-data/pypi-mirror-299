# read the contents of your README file
from os import path

from setuptools import find_packages, setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    lines = f.readlines()

# remove images from README
lines = [x for x in lines if ".png" not in x]
long_description = "".join(lines)

setup(
    name="omnigibson",
    version="1.0.0",
    author="Stanford University",
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/StanfordVL/OmniGibson",
    zip_safe=False,
    packages=find_packages(),
    install_requires=[
        "gymnasium>=0.28.1",
        "numpy<2.0.0,>=1.23.5",
        "scipy>=1.10.1",
        "GitPython~=3.1.40",
        "transforms3d~=0.4.1",
        "networkx~=3.2.1",
        "PyYAML~=6.0.1",
        "addict~=2.4.0",
        "ipython~=8.20.0",
        "future~=0.18.3",
        "trimesh~=4.0.8",
        "h5py~=3.10.0",
        "cryptography~=41.0.7",
        "bddl~=3.5.0",
        "opencv-python>=4.8.1",
        "nest_asyncio~=1.5.8",
        "imageio~=2.33.1",
        "imageio-ffmpeg~=0.4.9",
        "termcolor~=2.4.0",
        "progressbar~=2.5",
        "pymeshlab~=2022.2",
        "click~=8.1.3",
        "aenum~=3.1.15",
        "rtree~=1.2.0",
        "graphviz~=0.20",
        "numba>=0.60.0",
    ],
    extras_require={
        "isaac": ["isaacsim-for-omnigibson>=4.1.0"],
    },
    tests_require=[],
    python_requires=">=3",
    include_package_data=True,
)  # yapf: disable
