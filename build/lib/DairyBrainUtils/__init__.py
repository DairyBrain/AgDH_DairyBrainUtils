import logging
import sys
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy_utils.functions import database_exists

logger = logging.getLogger(__name__)


def get_engine(credentials):
    """
    Use sqlalchemy to create an engine instance for future database connection
    :param credentials: Dictionary with the following keys: [dialect, user, password, host, port, db_name, log]
    :return: An engine instance
    """
    try:
        db_engine = create_engine(
            credentials["dialect"]
            + "://"
            + credentials["user"]
            + ":"
            + credentials["password"]
            + "@"
            + credentials["host"]
            + ":"
            + credentials["port"]
            + "/"
            + credentials["db_name"],
            echo=credentials["log"],
        )
    except:
        logger.error("Can't connect to database: " + str(sys.exc_info()))
        sys.exit(1)
    return db_engine


def check_if_database_exists(db_engine):
    """
    Use existing sqlalchemy functionality to check if the database exists.
    :param db_engine: Specifies the connection to the database
    :return: True if database exists, False otherwise
    """
    return database_exists(db_engine.url)


def create_table_if_doesnt_exist(db_engine, table_name, sql_statement):
    """
    Creates a table with table_name in the database if a table with the given name doesn't exist.
    :param db_engine: Specifies the connection to the database
    :param table_name: Name of the table that needs to be created
    :param sql_statement: SQL statement with the column headers of the table. They are strings that are stored in the
    animal_import and event_import scripts.
    :return: None
    """
    # check and delete if table already exists
    if not has_table(table_name, db_engine):
        logger.debug("Table {} not found - creating...".format(table_name))

        with db_engine.connect() as con:
            try:
                logger.info("Creating table " + table_name + " in " + db_engine.url.database + " database...")
                logger.debug('create_temp_table_statement = ' + str(sql_statement.format(table_name)))
                con.execute(str(sql_statement.format(table_name)))
            except Exception as e:
                print("The exception is " + str(e))
                logger.error("Error creating the table " + table_name + " in " + db_engine.url.database + " database!")
                logger.error(e.args)
                exit(1)


def create_table(db_engine, table_name, sql_statement):
    """
    Creates a table with table_name in the database.
    :param db_engine: Specifies the connection to the database
    :param table_name: Name of the table that needs to be created
    :param sql_statement: SQL statement with the column headers of the table. They are strings that are stored in the
    animal_import and event_import scripts.
    :return: None
    """
    # check and delete if table already exists
    drop_table(table_name, db_engine)

    # create new temp table
    with db_engine.connect() as con:
        try:
            logger.info("Creating table " + table_name + " in " + db_engine.url.database + " database...")
            logger.debug('create_temp_table_statement = ' + str(sql_statement.format(table_name)))
            con.execute(str(sql_statement.format(table_name)))
        except Exception as e:
            print("The exception is " + str(e))
            logger.error("Error creating the table " + table_name + " in " + db_engine.url.database + " database!")
            logger.error(e.args)
            exit(1)


def create_schema(db_engine, schema_name):
    """
    Creates a schema in the database
    :param db_engine: Specifies the connection to the database
    :param schema_name: Name of the schema to be created
    :return: None
    """
    with db_engine.connect() as con:
        try:
            logger.info("Creating schema " + schema_name)
            con.execute(text("CREATE SCHEMA IF NOT EXISTS " + schema_name + ";"))
        except Exception as e:
            print("The exception is " + str(e))
            logger.error("Error creating the schema " + schema_name)
            logger.error(e.args)
            exit(1)


def create_sequence(db_engine, sequence_name):
    """
    Creates a sequence in the database
    :param db_engine: Specifies the connection to the database
    :param sequence_name: Name of the sequence to be created
    :return: None
    """
    with db_engine.connect() as con:
        try:
            logger.info("Creating sequence " + sequence_name)
            con.execute(text("CREATE SEQUENCE IF NOT EXISTS " + sequence_name + ";"))
        except Exception as e:
            print("The exception is " + str(e))
            logger.error("Error creating the sequence " + sequence_name)
            logger.error(e.args)
            exit(1)


def get_next_from_sequence(db_engine, sequence_name):
    """
    Returns the next id in the given sequence (assuming one exists)
    :param db_engine: Specifies the connection to the database
    :param sequence_name: Name of the sequence to be created
    :return: None
    """
    query_sequence_statement = text("SELECT nextval(\'" + sequence_name + "\');")

    with db_engine.connect() as con:
        try:
            logger.info("Creating query_sequence_statement...")
            # Optional error checking here to check if the sequence exists
            result = con.execute(query_sequence_statement)
            row = result.fetchone()
            if type(row[0]) is not int:
                logger.error("Error getting an integer id from sequence!")
                exit(1)
            return row[0]
        except Exception as e:
            logger.error("Error creating query_sequence_statement!")
            logger.error(e)
            exit(1)


def populate_table_from_csv(table_name, csv_location, db_engine):
    """
    Populates a table with the contents of a csv file
    :param table_name: Name of the table that needs to be populated
    :param csv_location: Location of the csv file
    :param db_engine: Specifies the connection to the database
    :return: None
    """
    # 'copy_from' example from https://www.dataquest.io/blog/loading-data-into-postgres/
    # adapted to sqlalchemy using https://stackoverflow.com/questions/13125236/sqlalchemy-psycopg2-and-postgresql-copy
    with db_engine.connect() as con:
        # isolate a connection
        connection = db_engine.connect().connection

        # get the cursor
        cursor = connection.cursor()

        try:
            with open(csv_location, 'r') as f:
                next(f)  # Skip the header row.
                cursor.copy_from(f, table_name, sep=',', null='')
            connection.commit()

        except Exception as e:
            logger.error(
                "Error importing the table " + table_name + " in " + db_engine.url.database +
                " database from " + csv_location + "!")
            logger.error(e.args)
            exit(1)


def execute_statement(statement, db_engine):
    """
    Executes a SQL statement in the database
    :param statement: String; SQL statement
    :param db_engine: Specifies the connection to the database
    :return: None
    """
    with db_engine.connect() as con:
        try:
            con.execute(text(statement))
        except Exception as e:
            logger.error("Error executing statement {}".format(statement))
            logger.error(e.args)
            exit(1)


def drop_table(table_name, db_engine):
    """
    Drops a table from the database
    :param table_name: Name of the table that needs to be dropped
    :param db_engine: Specifies the connection to the database
    :return: None
    """
    if has_table(table_name, db_engine):
        logger.debug("Deleting old (pre-existing) table: " + table_name + "...")
        statement = str("DROP TABLE IF EXISTS {};")

        with db_engine.connect() as con:
            try:
                con.execute(statement.format(table_name))
            except Exception as e:
                logger.error("Error deleting table " + table_name + " from database!")
                logger.error(e.args)
                exit(1)


def has_table(table_name, db_engine):
    """
    Checks if a table with table_name is in the database
    :param table_name: Name of the table that needs to be checked
    :param db_engine: Specifies the connection to the database
    :return: True if table with table_name is in the database, False otherwise
    """
    if '.' in table_name:  # received schema.table_name
        return db_engine.has_table(table_name.split('.')[1], schema=table_name.split('.')[0])
    else:  # received plain table_name
        return db_engine.has_table(table_name)
