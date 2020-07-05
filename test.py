import dns
import secret
from pymongo import *

def get_one_book(client, bookID):
  print(client.Library.Books.find_one({"_id":bookID}))

client = MongoClient("mongodb+srv://{0}:{1}@cluster0.yyt0d.mongodb.net/Library?retryWrites=true&w=majority".format(secret.username, secret.password))

get_one_book(client, "19335MEE")