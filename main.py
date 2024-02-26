from fastapi import FastAPI
from config import config
import psycopg2

app = FastAPI()

def retrieve_all_data():
    try:
        connection = None
        params = config()
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()

        print('Executing Query')
        cursor.execute("SELECT * FROM subwaydata")
        print('Query executed')

        rows = cursor.fetchall()

    except(Exception, psycopg2.DatabaseError) as error:
        return error

    finally:
        cursor.close()
        connection.close()

    return rows

def retrieve_one_data(location_name):
    try:
        connection = None
        params = config()
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()

        print('Executing Query')
        cursor.execute("SELECT * FROM subwaydata WHERE location_name = %s", (location_name,))
        print('Query executed')

        current_row = cursor.fetchone()

    except(Exception, psycopg2.DatabaseError) as error:
        return error
    
    finally:
        cursor.close()
        connection.close()

    return current_row


@app.get("/subway-data/all")   # function below is handling get request
# async used in case of multiple input or output operations
async def read_all_data():
    return retrieve_all_data()
        

@app.get("/subway-data/{location_name}")
async def read_one_data(location_name):
    return retrieve_one_data(location_name)

# print(retrieve_one_data("Subway Jln Pinang"))

## uvicorn main:app --reload

## Setup front end
"""
Install Vue by node install -g @vue/cli
Create project by vue create proj-name
"""