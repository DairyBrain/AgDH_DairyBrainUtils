# AgDH_DairyBrainUtils

## About
AgDH_DairyBrainUtils is a PyPI package with some basic functionalities for interacting with a database along with some other Dairy-Brain-specific utilities.

## Usage
To install the package, do:

`pip3 install -i https://test.pypi.org/simple/ DairyBrainUtilities-ruipeterpan==0.0.4`

Once installed, we recommend you to import the package with `import DairyBrainUtils as dbu`.

A list of functions that are available for use are:

* `create_table_if_doesnt_exist(db_engine, table_name, sql_statement)`
* `create_table(db_engine, table_name, sql_statement)`
* `populate_table_from_csv(table_name, csv_location, db_engine)`
* `execute_statement(statement, db_engine)`
* `drop_table(table_name, db_engine)`
* `has_table(table_name, db_engine)`
* `create_schema(db_engine, schema_name)`

In the above signatures, `db_engine` is an engine instance created by sqlalchemy. For more info, refer to [this](https://kite.com/python/docs/sqlalchemy.create_engine) document.

## Development
See [this](https://packaging.python.org/tutorials/packaging-projects/) tutorial for guidance on packaging a Python project and uploading it to the PyPI (Python Package Index).
[This](https://github.com/pypa/sampleproject) is a sample project with the best format.


To publish a new version of the package, edit `./DairyBrainUtils/__init__.py`, change the version number in `setup.py`, and publish the distribution archives following the tutorial.

More specifically, do:

```
python3 -m pip install --upgrade setuptools wheel
python3 setup.py sdist bdist_wheel
```
Now, a `dist` directory should be created with two files. If the package is to be hosted on a local server, just take the `.whl` file and use `pip` to [install](https://stackoverflow.com/questions/27885397/how-do-i-install-a-python-package-with-a-whl-file) the package. 

For uploading the distribution packages to TestPyPI, do:
```
python3 -m pip install --upgrade twine
python3 -m twine upload --repository testpypi dist/*
```

Use `__token__` when prompted to enter the username. For the password, use the token value, including the `pypi-` prefix.




