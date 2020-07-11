import dns
import secret
import random
import string
from dbhandler import *
from pymongo import *

client = MongoClient("mongodb+srv://{0}:{1}@cluster0.yyt0d.mongodb.net/Library?retryWrites=true&w=majority".format(secret.username, secret.password))

renew_loan(client, "A73474TER", "00002CHA")