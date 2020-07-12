import dns
import secret
import random
import string
from dbhandler import *

client = MongoClient("mongodb+srv://{0}:{1}@cluster0.yyt0d.mongodb.net/Library?retryWrites=true&w=majority".format(secret.username, secret.password))
def return_loan(client, user_id, book_id):
    #Retrieve loan
    loans = client.Library.Users.find_one({"_id": user_id}, {
        "_id":0,
        "loans":1
    })["loans"]
    [loan] = [i for i in loans if i ["book_id"]==book_id]
    #Remove loan from user
    client.Library.Users.update_one(
        {"_id": user_id},
        {
        "$pull": {"loans": {"$elemMatch": {"book_id": book_id}}},
        }
    )
    #Mark book as available
    client.Library.Books.update_one(
        {"_id":book_id},
        {
        "$set":{"avail": True}
        }
    )
    #Modify loan object to prepare for archival
    loan["return"] = datetime.datetime.utcnow()
    loan["user_id"] = user_id
    #Push to loans DB meant for past loans
    client.Library.Loans.insert_one(loan)
    print("Successfully returned book")

#return_loan(client, "A73474TER", "00001MAR")
client.Library.Users.update_one(
        {"_id": "A73474TER"},
        {
        "$pull": {"loans": {"book_id": "00002CHA"} },
        "$dec": {"loan_num": 1}
        }
)
print("done")