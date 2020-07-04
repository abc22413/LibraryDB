from cliagent import *
import dns
import secret
from pymongo import *
from errors import *

if __name__ == "__main__":
  client = None
  try:
    #Welcome message
    show_welcome()
    time.sleep(1.5)

    #Connect to DB
    client = MongoClient("mongodb+srv://john:john@cluster0.yyt0d.mongodb.net/Library?retryWrites=true&w=majority")
    if not client.Library.test:
      raise DBConnectionError

    #Start main program
    start_cli(client)
    client.close()

  except DBConnectionError:
    print("Error connecting to database")

  finally:
    #End of program
    print("\nThank you for visiting ABC Libary")
    print("Session ended {}".format(datetime.now().strftime("%d %B %Y %H:%M:%S")))
