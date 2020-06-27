import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DairyBrainUtils-ruipeterpan",
    version="0.3.0",
    author="Rui Pan",
    author_email="rpan33@wisc.edu",
    description="A set of functions that interacts with a database. It contains some basic functionalities along with some other Dairy-Brain-specific functionalities.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DairyBrain/AgDH_DairyBrainUtils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
