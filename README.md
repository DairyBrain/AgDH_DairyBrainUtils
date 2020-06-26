# AgDH_DairyBrainUtils

- [AgDH_DairyBrainUtils](#agdh-dairybrainutils)
  * [About](#about)
  * [Installation](#installation)
  * [Documentation](#documentation)
  * [Development](#development)



## About
DairyBrainUtils is a PyPI package with some basic functionalities for interacting with a PostgreSQL database.

For now, it is hosted on TestPyPI. If the TestPyPI distribution got cleaned up, please contact the author to re-upload it.

## Installation
To install the latest version of the package, use the command in [TestPyPI](https://test.pypi.org/project/DairyBrainUtils-ruipeterpan/).

If the above link is broken, try:

`pip3 install -i https://test.pypi.org/simple/ DairyBrainUtilities-ruipeterpan==0.1.1`

Once installed, we recommend you to import the package with `import DairyBrainUtils as dbu`.



## Documentation

A list of functions that are available for use are:

* `get_engine(credentials)`
* `create_table_if_doesnt_exist(db_engine, table_name, sql_statement)`
* `create_table(db_engine, table_name, sql_statement)`
* `populate_table_from_csv(table_name, csv_location, db_engine)`
* `execute_statement(statement, db_engine)`
* `drop_table(table_name, db_engine)`
* `has_table(table_name, db_engine)`
* `create_schema(db_engine, schema_name)`

####`get_engine(credentials)`
Takes in a dictionary `credentials` with the keys: `[dialect, user, password, host, port, db_name, log]`, and passes these
credentials into [sqlalchemy.create_engine()](https://kite.com/python/docs/sqlalchemy.create_engine) to create a new engine instance.
* `dialect`: String. A database dialect. Right now this package only supports `postgresql`.
* `user`: String. The username of a user in the database.
* `password`: String. The password that is associated with the user.
* `host`: String. Host name.
* `port`: Integer. Port number.
* `db_name`: String. A database name.
* `log`: Boolean. If True, the engine will log all statements as well as a repr() of their parameter lists to the engines logger, which defaults to sys.stdout.

####create_table_if_doesnt_exist(db_engine, table_name, sql_statement)
Creates a table with `table_name` in the database if a table with the given name doesn't exist.

`sql_statement` is a `CREATE TABLE` statement that specifies the headers of the table to be created.

####create_table(db_engine, table_name, sql_statement)

Creates a table with table_name in the database.

`sql_statement` is a `CREATE TABLE` statement that specifies the headers of the table to be created.

####populate_table_from_csv(table_name, csv_location, db_engine)

Takes in a `csv_location`, the file path of a csv file, and populates the table with the given `table_name` (assuming one exists) in the specified database.

####execute_statement(statement, db_engine)

Executes a SQL statement in the specified database.

####drop_table(table_name, db_engine)

Drops a table with `table_name` in the specified database.

####has_table(table_name, db_engine)

Returns `True` if there exists a table with the given `table_name` in the specified database, returns `False` otherwise

####create_schema(db_engine, schema_name)

Creates a schema with the given `schema_name` in the specified database.


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
