from cliagent import *
import dns
import secret
from pymongo import *
from errors import *

if __name__ == "__main__":
  client = None
  try:
    client = MongoClient("mongodb+srv://john:john@cluster0.yyt0d.mongodb.net/Library?retryWrites=true&w=majority")
    if not client.test():
      raise DBConnectionError
    start_cli(client)
    client.close()
  except DBConnectionError:
    print("Error connecting to database")