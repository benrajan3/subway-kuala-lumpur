# subway-kuala-lumpur
The system mainly displays all of the available outlets of Subway in Kuala Lumpur. It also allows the user to search for specific outlets. The output of the outlet search would be 
- Name of the outlet
- Address of the outlet
- Operating hours of the outlet
- Waze link of the outlet
- Geolocation of the outlet

## Setting up environment
The file `requirements.txt` contains all the neccessary libraries to run the program.

### Create virtual environment
1. To create a virtual environment, type in the terminal `python3 -m venv virtual-environment-name` 
2. To activate the virtual environment,
    1. MacOS
        - Type in `source virtual-environment-name/bin/activate`
    2. Windows
        - Type in `.\venv\Scripts\activate`

### Install all dependencies
1. Python with FastAPI and psycopg2-binary  
    1. Ensure that Python is installed in the system
        1. To check for Python, type in the terminal, `python --version` or `python3 --version`
    2. To install all dependencies to run the system, type in the terminal `pip install -r requirements.txt`
    3. Check that all libraries in the Python file are compiled correctly without showing errors.

2. Vue 3 with npm
    1. Ensure that the system has npm and Node
        1. To check for npm, type in the terminal, `npm --version`
        2. To check for node, type in the terminal, `node --version`
    2. Install Vue 3 on the system
        1. In the terminal, type in `npm install -g @vue/cli`
    3. Install all dependencies found in package.json
        1. In the terminal, type in `npm install`
    4. Compile and run the Vue app to ensure dependencies are installed correctly.
        1. In the terminal, type in `npm run serve`

## Data Scraping from Website
With the given URL, data of each outlets are scrape from the website to be pushed into a database.

### Data Scraping from URL
Parsed the content retrieved from the URL to a new HTML file. Outlet's data is retrieved from map function in the script tag. Data retrieved is converted to JSON to retrieved the values of each key. To retreive specific values of the outlet, indexing is required by using the `.find()` built-in function.

### Connecting script to PostgreSQL
The parameters of the database such as host, port, username, password, database name is required to connect the database. Database has to be created before connecting the database.
1. Install PostgreSQL and pgAdmin 4 to create the master username and password.
2. In the terminal, type in `psql -U postgres` and enter the password.
3. To create a new database, type in `CREATE DATABASE db-name`
4. Check if the database has been created, type in `\l`
5. Exit the psql shell by typing, `exit` or `\q`

### Creating database, tables and inserting values
Using the `psycopg2` library as a driver to connect to PostgreSQL. Creata a connection with the database and initialise a cursor to execute queries. Create a new table if it is not found in the database. For every outlet's data retrieved, the data is being inserted to the table. At the end, the changes made to the table is committed and the connection will be closed. 

## Serve data via REST APIs using FastAPI
The back-end framework is using FastAPI. The filename for the API is `subway-kuala-lumpur/main.py`. 
To run the back-end,
1. In the terminal, type in `uvicorn main:app --reload` where main is the filename.

There are two APIs found in the back-end
1. Retrieve all data
    1. URL: http://localhost:8000/subway-data/all
    2. The API will connect to the database where all the outlet's data is populated.
    3. Then, it will fetch all data found in the table
    4. Data will be returned in a list type where every element in the list is data of an outlet.

2. Retrieve specific outlet data using outlet's name
    1. URL: http://localhost:8000/subway-data/{location_name}
    2. As an example, http://localhost:8000/subway-data/Subway Jln Pinang
    3. The API will connect to the database where all the outlet's data is populated.
    4. Then, it will fetch one data following the specified location name in the parameter of the URL.
        - If the location name is not found, it will return an error message from psycopg2
    5. Data will be returned in a list type where the first element is the data of the specified outlet. 

## Retrieve data from API to display on map using Vue 3
The front-end framework is using Vue 3. Please move to `cd frontendvue/subway-map`
To run the front-end, type in `npm run serve`

There are two components found in the current version of the front-end,
1. Navbar
    - Navbar shows the navigation bar consisting the logo of Subway and header of the application name, "Subway Kuala Lumpur Locations".
    - The Navbar is being imported to the App.vue to be shown in the front-end

2. Map
    - The base map object is MapTiler. Initialising the map with the provided `API-KEY` and a fixed longitude and latitude value of Kuala Lumpur. 
