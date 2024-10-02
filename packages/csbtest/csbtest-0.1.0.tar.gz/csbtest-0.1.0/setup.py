from setuptools import setup, find_packages

setup(
    name="csbtest",            # Name of your package
    version="0.1.0",                # Version number
    description="Crowdsourced bathymetry toolkit",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Vishwa Barathy",
    author_email="vishwa.barathy@cidco.ca",
    packages=find_packages(),       # Automatically find packages
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
