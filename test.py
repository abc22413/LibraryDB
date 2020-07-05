from pymongo import *
import secret
import dns
import random

client = MongoClient("mongodb+srv://{0}:{1}@cluster0.yyt0d.mongodb.net/Library?retryWrites=true&w=majority".format(secret.username, secret.password))

for i in client.Library.test.find({}):
  print(i)

new = {
    "_id": "00001MAR",
    "title": "Gilead",
    "authors": ["Marilynne Robinson"],
    "avail": True,
    "pgs": 247,
    "isbn": "9780002005883"
}
retry = 0
while retry<5:
  try:
    retry+=1
    success = client.Library.test.insert_one(new).inserted_id
    print(success)
    break
  except:
    new["_id"] = str(random.randint(1,99999)).zfill(5)+new["authors"][0].replace(" ","")[:3].upper()
    continue
  finally:
    input("Press Enter to continue")