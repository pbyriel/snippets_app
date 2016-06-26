import logging
import argparse
import psycopg2

#set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)

#connect to db
logging.debug("Connecting to PostgreSQL.")
connection = psycopg2.connect(database="snippets")
logging.debug("Database connection established.")



def put(name, snippet):
    """
    Store a snippet with an associated name.
    Returns the name and the snippet
    """
    logging.info("Storing snippet {!r}: {!r}".format(name, snippet))
    cursor = connection.cursor()
    command = "insert into snippets values (%s, %s)"
    cursor.execute(command, (name, snippet))
    connection.commit()
    logging.debug("Snippets stored succesfully.")
    #logging.error("FIXME: Unimplemented - put({!r}, {!r})".format(name, snippet))
    return name, snippet
    

def get(name):
    """
    Retrieve the snippet with a given name.
    If there is no such snippet, return '404: Snippet Not Found'
    Returns the snippet.
    """
    logging.info("Retrieving snippet {!r}.".format(name))
    cursor = connection.cursor()
    command = "select message from snippets where keyword = (%s)"
    cursor.execute(command, (name,))
    snippet = cursor.fetchone()
    #logging.error("FIXME: Unimplemented - get({!r})".format(name))
    return snippet

    
def main():
    """Main function"""
    logging.info("Constructing parser")
    parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    #subparser for the put command
    logging.debug("Constructing put parser")
    put_parser = subparsers.add_parser("put", help="Store a snippet")
    put_parser.add_argument("name", help="Name of snippet")
    put_parser.add_argument("snippet", help="Snippet text")
    
    #subparser for the get command
    logging.debug("Constructing get parser")
    get_parser = subparsers.add_parser("get", help="Retrieve a snippet")
    get_parser.add_argument("name", help="Name of snippet")
    
    
    arguments = parser.parse_args()
    # Convert parsed arguments from Namespace to dictionary
    arguments = vars(arguments)
    command = arguments.pop("command")
    
    if command == "put":
        name, snippet = put(**arguments)
        print("Stored {!r} as {!r}".format(snippet, name))
    elif command == "get":
        snippet = get(**arguments)
        print("Retrieved snippet: {!r}".format(snippet))
    
    

if __name__ == '__main__':
    main()