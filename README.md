# AgDH_database_functions

See [this](https://packaging.python.org/tutorials/packaging-projects/) tutorial for guidance on packaging a Python project and uploading it to the PyPI (Python Package Index).
[This](https://github.com/pypa/sampleproject) is a sample project with the best format.

For the /dist directory, the tar.gz file is a source archive whereas the .whl file is a built distribution. Newer pip versions preferentially install built distributions, but will fall back to source archives if needed. You should always upload a source archive and provide built archives for the platforms your project is compatible with. In this case, our example package is compatible with Python on any platform so only one built distribution is needed.

## About
AgDH_database_functions is a PyPI package with some basic functionalities for interacting with a database along with some other Dairy-Brain-specific functionalities.

## Placeholder for an actual README