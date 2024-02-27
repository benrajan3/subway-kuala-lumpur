import requests
from bs4 import BeautifulSoup
import json
from config import config
import psycopg2


def filter_kl(text):
    if "Kuala Lumpur" in text:
        return True
    else:
        return False
    
def scrape_connect_db(url_connection):
    
    # Initialise connection with DB
    try:
        connection = None
        params = config()
        connection = psycopg2.connect(**params)     # everything in params into connect function arguments
        print('Database connected')
        cursor = connection.cursor()
        cursor.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name='subwaydata')")
        table_exists = cursor.fetchone()[0]

        # Create the table if it is not found in the database
        if table_exists:
            print('Table is found')
            # cursor.close()
            # connection.close()
            # print('Connection closed')
        else:
            print('Creating table...')
            cursor.execute("CREATE TABLE subwaydata(id INT PRIMARY KEY, location_name TEXT, address TEXT, operating_hours TEXT, waze_link TEXT, geolocation JSONB)")
            connection.commit()
            cursor.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name='subwaydata')")
            table_exists_after_creation = cursor.fetchone()[0]
            print(f'Table created?: {table_exists_after_creation}')
            # cursor.close()
            # connection.close()
            # print('Connection closed')

        
    except(Exception, psycopg2.DatabaseError) as error:
        connection.rollback()
        print(error)



    # Replace with the actual URL
    url = url_connection
    
    response = requests.get(url)
    
    # Parse the HTML
    soup = BeautifulSoup(response.content, "html.parser")
    with open("copy.html", "w") as f:
        f.write(str(soup))

    """
    html_content = 
    <script>
    map.init(//my content here);
    </script>
    """
    with open("copy.html", "r") as f:
        html_content = f.read()

    start_index = 0
    while True:    
        start_index = html_content.find("map.init(", start_index)
        if start_index == -1:
            break  

        end_index = html_content.find(");", start_index + len("map.init("))
        if end_index == -1:
            print("Error: Unmatched quote")
            break

        extracted_content = html_content[start_index + len("map.init("):end_index]
        start_index = end_index + 1  # Move to the next potential occurrence

    # Try converting the string to JSON
    try:
        json_data = json.loads(extracted_content)
    except json.JSONDecodeError as e:
        print("Error converting string to JSON:", e)

    marker_data_lst = json_data['markerData']

    for marker in marker_data_lst:
        subway_content = marker["infoBox"]["content"]
        if filter_kl(subway_content) == True:
            location_id = marker["id"]
            # print(location_id)

            start_loc_index = subway_content.find('<h4>') + len('<h4>')  # find index starts from <. Then add the length of tag to retrieve the first index of name
            end_loc_index = subway_content.find('</h4>')
            loc_name = subway_content[start_loc_index:end_loc_index]
            # print(loc_name)

            start_add_index = subway_content.find('<p>') + len('<p>')
            end_add_index = subway_content.find('</p>')
            address = subway_content[start_add_index:end_add_index]
            # print(address)

            p_split = subway_content.split('<p>')
            unfiltered_hours = p_split[3]
            start_op_index = 0
            end_op_index = unfiltered_hours.find('</p>')
            operating_hours = unfiltered_hours[start_op_index:end_op_index]
            # print(operating_hours)

            href_split = subway_content.split('href=')
            unfiltered_waze = href_split[3]
            start_waze_index = 0
            end_waze_index = unfiltered_waze.find('>')
            waze_link = unfiltered_waze[start_waze_index:end_waze_index]
            # print(waze_link)

            geographical_pos = marker["position"]
            json_geolocation = json.dumps(geographical_pos)
            # print(geographical_pos)

            # print("###### NEXT SUBWAY LOCATION ######")
            cursor.execute("SELECT 1 FROM subwaydata WHERE id = %s", (location_id,))
            row_exists = cursor.fetchone()

            if row_exists:
                continue
            else:
                cursor.execute("INSERT INTO subwaydata (id, location_name, address, operating_hours, waze_link, geolocation) VALUES (%s, %s, %s, %s, %s, %s)", (location_id, loc_name, address, operating_hours, waze_link, json_geolocation))

    connection.commit()
    print("Values have been inserted into the database successfully!")


    cursor.close()
    connection.close()
    print('Connection closed')

       
scrape_connect_db("https://subway.com.my/find-a-subway")
# https://www.postgresqltutorial.com/postgresql-python/connect/
# Connecting PostgreSQL to Python 
# DB name: subway
             


