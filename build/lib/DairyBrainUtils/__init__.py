import csv
import logging
from sqlalchemy.sql import text
import ntpath

logger = logging.getLogger(__name__)


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
                con.execute(text(sql_statement.format(table_name)))
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
            con.execute(text(sql_statement.format(table_name)))
        except Exception as e:
            print("The exception is " + str(e))
            logger.error("Error creating the table " + table_name + " in " + db_engine.url.database + " database!")
            logger.error(e.args)
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
        statement = "drop table if exists {};"

        with db_engine.connect() as con:
            try:
                con.execute(statement.format(table_name))
            except Exception as e:
                logger.error("dc_event_import.drop_table(): Error deleting table " + table_name + " from database!")
                logger.error(e.args)
                exit(1)


def has_table(table_name, db_engine):
    """
    Checks if a table with table_name is in the database
    :param table_name: Name of the table that needs to be checked
    :param db_engine: Specifies the connection to the database
    :return: True if table with table_name is in the database, False otherwise
    """
    return db_engine.has_table(table_name.split('.')[1], schema=table_name.split('.')[0])


# def check_for_fixed_file(in_filename, out_filename, filelist, type):
#     """
#     Checks if file passed in is already fixed. If fixed, returns the file name; otherwise, calls the respective fix
#     function in dc_file_fix and returns the filename after the fix.
#     :param filename: The name of the file that need to be checked
#     :param filelist: A list of strings of the filenames of the files that need to be parsed (sorry bad engrish)
#     :param type: Integer, specifies the type of the source file (1 for animal, 2 for active animal, 5&6 for events). A
#     potential enhancement is to check the integer at the end of the filename instead of hard-coding it
#     :return: Filename of the fixed file
#     """
#     # if this one isn't fixed
#     if ntpath.basename(in_filename).split('.')[-1] == 'fixed':
#         return in_filename
#     else:
#         # and there isn't an equivilant fixed file in the list
#         if in_filename + ".fixed" not in filelist:
#             # create a fixed file
#             if type == 1 or type == 2:
#                 return fix_animal_file(in_filename, out_filename)
#             elif type == 5 or type == 6:
#                 return fix_event_file(in_filename, out_filename)
#             else:
#                 logger.error("Bad file: File type not supported (should be animal/active_animal/event)")
#                 exit(1)
#         else:
#             # it'll get to the fixed on on it's own
#             return None


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


# def fix_animal_file(in_filename, out_filename):
#     """
#
#     :param in_filename:
#     :param out_filename:
#     :return:
#     """
#     with open(out_filename, "w+") as out_csv:
#         csv_writer = csv.writer(out_csv, delimiter=',')
#         with open(in_filename) as in_csv:
#             csv_reader = csv.reader(in_csv, delimiter=',')
#             num_columns = 0
#             for row in csv_reader:
#                 row.pop()
#                 if row[0][0:5] != 'Total':
#                     if num_columns == 0:
#                         num_columns = len(row)
#                         logger.debug("Set row count to: " + str(num_columns))
#                     elif len(row) > num_columns:
#                         logger.debug("unshrunk row: " + str(row))
#                         shrunk_row = shrink_animal_row(row, num_columns)
#                         logger.debug("shrunk row: " + str(shrunk_row))
#                     elif len(row) < num_columns:
#                         logger.error("Row has too few columns!")
#                         logger.error("row = " + str(row))
#                         exit(1)
#                     for pos in range(len(row)):
#                         row[pos] = row[pos].strip()
#                     logger.debug("writing row: " + str(row))
#                     csv_writer.writerow(row)
#     return out_filename
#
#
# def shrink_animal_row(row, num_columns):
#     """
#
#     :param row:
#     :param num_columns:
#     :return:
#     """
#     # how many extra rows?
#     extra_row_count = len(row) - num_columns
#     if extra_row_count > 0:
#         remark = row[15] + " "
#         for i in range(extra_row_count):
#             remark += row.pop(16)
#         row[8] = remark
#     return row
#
#
# def fix_event_file(in_filename, out_filename):
#     """
#
#     :param in_filename:
#     :param out_filename:
#     :return:
#     """
#     with open(out_filename, "w+") as out_csv:
#         csv_writer = csv.writer(out_csv, delimiter=',')
#         with open(in_filename) as in_csv:
#             csv_reader = csv.reader(in_csv, delimiter=',')
#             num_columns = 0
#             for row in csv_reader:
#                 row.pop()
#                 if num_columns == 0:
#                     num_columns = len(row)
#                     logger.debug("Set row count to: " + str(num_columns))
#                 elif len(row) > num_columns:
#                     logger.debug("unshrunk row: " + str(row))
#                     shrunk_row = shrink_row(row, num_columns)
#                     logger.debug("shrunk row: " + str(shrunk_row))
#                 elif len(row) < num_columns:
#                     logger.error("Row has too few columns!")
#                     logger.error("row = " + str(row))
#                     exit(1)
#                 for pos in range(len(row)):
#                     row[pos] = row[pos].strip()
#                 logger.debug("writing row: " + str(row))
#                 csv_writer.writerow(row)
#     return out_filename
#
#
# def shrink_row(row, num_columns):
#     """
#
#     :param row:
#     :param num_columns:
#     :return:
#     """
#     # how many extra rows?
#     extra_row_count = len(row) - num_columns
#     if extra_row_count > 0:
#         remark = row[8] + " "
#         for i in range(extra_row_count):
#             remark += row.pop(9)
#         row[8] = remark
#     return row