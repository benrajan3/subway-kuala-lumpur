from configparser import ConfigParser

def config(filename="database.ini", section="postgresql"):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    # iterate over the filename to retrieve the data
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1] # assign each value into key of the db dict

    else:
        raise Exception(f'Section{0} is not found in the {1}'.format(section,filename))

    return db
