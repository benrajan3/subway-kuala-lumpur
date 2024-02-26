import psycopg2
from config import config
# Creates a new database connection session

def connect():
    connection = None
    try:
        params = config()
        print('Connecting to PostgreSQL Database...')
        connection = psycopg2.connect(**params) # everything in params into connect function arguments

        # create a cursor
        crsr = connection.cursor()
        print('PostgreSQL version:')
        crsr.execute('SELECT version()')
        db_version = crsr.fetchone()
        print(db_version)
        crsr.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
            print('Database connection terminated')

if __name__ == "__main__":
    connect()
