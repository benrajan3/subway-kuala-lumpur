import psycopg2
from config import config


def connect_add_data():
    try:
        connection = None
        params = config()
        connection = psycopg2.connect(**params)
        # print(connection)
        crsr = connection.cursor()
        crsr.execute("CREATE TABLE person")





        connection.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)

connect_add_data()