import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dairybrain-database-functions-ruipeterpan", # Replace with your own username
    version="0.0.1",
    author="Rui Pan",
    author_email="rpan33@wisc.edu",
    description="A set of functions that interacts with a database. It contains some basic functionalities along with some other Dairy-Brain-specific functionalities.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DairyBrain/AgDH_database_functions",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)