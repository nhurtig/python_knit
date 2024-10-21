"""For package installation"""

from setuptools import setup, find_packages

setup(
    name="python_knit",
    version="0.1",
    packages=find_packages(where="src"),
    package_data={
        "braid": ["py.typed"],
        "braid.canon": ["py.typed"],
        "category": ["py.typed"],
        "common": ["py.typed"],
        "fig_gen": ["py.typed"],
        "layer": ["py.typed"],
    },
    include_package_data=True,
    zip_safe=False,
    package_dir={"": "src"},
)
