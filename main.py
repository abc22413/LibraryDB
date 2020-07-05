#Run main code
from cliagent import *
import secret
from errors import *

if __name__ == "__main__":
  client = None
  try:
    #Welcome message
    show_welcome()
    time.sleep(0.8)

    #Connect to DB
    client = MongoClient("mongodb+srv://{0}:{1}@cluster0.yyt0d.mongodb.net/Library?retryWrites=true&w=majority".format(secret.username, secret.password))
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
