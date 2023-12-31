import mysql.connector as mysql

from config import *
import csv

# Function to connect to MySQL server and optionally, database
def connection(database=None):
    args = {
        'host': HOST,
        'port': PORT,
        'user': USER,
        'password': PASSWORD,
        'use_pure': True
    }
    if database:
        args['database'] = database
    return mysql.connect(**args)

# Trying Connecting to MySQL server with credentials in config file
# Connection to start as soon as this script is imported
try:
    print(f"Connecting to MySQL server on {HOST}:{PORT}...")
    conn = connection()
except mysql.errors.ProgrammingError:
    print("MySQL User or password incorrect in config.ini")
    exit()
except mysql.errors.InterfaceError:
    print("Can't connect to the MySQL Server.")
    print("Make sure that the server is running")
    exit()

# Function to create new Database
def createDB():
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE {DATABASE}")
    cursor.close()

# Function to run a sql script

def callproce(case_id, p_o_c, det_id, case_details):
    cursor = conn.cursor()
    try:
        case_id = case_id
        p_o_c = p_o_c
        det_id = det_id
        case_details = case_details

        # Call the stored procedure
        result = cursor.callproc("InsertNewCase", (case_id, p_o_c, det_id, 0, case_details))
        print(result)

        print("Stored procedure executed successfully")

    except Exception as e:
        print(f"Error: {e}")
def source(filename, *args, output=True, lastRowId=False):
    cursor = conn.cursor(buffered=output)
    with open('sql/' + filename) as f:
        statements = f.read()
        statements = statements.replace('\n', ' ')
        statements = statements.replace(';', '\n')
        for statement in statements.strip().splitlines():
            if args:
                cursor.execute(statement, args) if statement else None
                break
            cursor.execute(statement) if statement else None

    if output:
        result = cursor.fetchall()
    if lastRowId:
        result = cursor.lastrowid
    conn.commit()
    cursor.close()
    if output or lastRowId:
        return result

def clear():
    global conn
    cur = conn.cursor()
    cur.execute(f"DROP DATABASE IF EXISTS {DATABASE}")
    cur.close()
    createDB()
    conn = connection(DATABASE)
    source('tables_schema.sql', output=False)


# This section will run as soon as this script is imported
# To check if the database for this app exists or not
# The name of database is taken from the config file
# If not existing already (e.g. running this app for the first time),
# automatically creates the database and tables
# Also connects to the database of MySQL server
print(f"Connecting to {DATABASE} database...")
cur = conn.cursor(buffered=True)
newDB = False
cur.execute("SHOW DATABASES")
if (DATABASE,) not in cur.fetchall():
    print(f"No database named {DATABASE} found. Creating Database...")
    createDB()
    newDB = True
cur.close()
conn.close()
conn = connection(DATABASE)
if newDB:
    print("Creating required tables in the database...")
    source('tables_schema.sql', output=False)


# Running this script explicitly to delete the database
# Implemented for developement purposes only
# No need to run this script explicitly in production
if __name__ == '__main__':
    # Getting confirmation from the user
    print("Running this script explicitly will delete the database with name as in config.ini")
    x = input("Do you want to delete the database? [Y/n] ").upper()
    if x == 'Y' or x == 'YES':
        # Deleting the database with name as in config file
        cur = conn.cursor()
        cur.execute(f"DROP DATABASE IF EXISTS {DATABASE}")
        cur.close()
        print("database deleted")
    print(conn)
    conn.close()
