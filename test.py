import dns
import secret
import random
import string
from pymongo import *

def gen_new_userID(userobj):
  #(random Letter)99999ABC
  name=userobj["name"]
  name="".join([i for i in name if i not in [",./';-"]]).upper()
  userobj["_id"] = random.choice(string.ascii_uppercase)+str(random.randint(1,99999)).zfill(5)+name[:3]
  return userobj

def create_user(client, new_user):
  new_user = gen_new_userID(new_user)
  try:
    success = client.Library.Users.insert_one(new_user).inserted_id
    print("Successfully added user with User ID {0}".format(success))
  except:
    pass
    #print("Failed to make new user")
  finally:
    pass
    #input("Press Enter to continue")

client = MongoClient("mongodb+srv://{0}:{1}@cluster0.yyt0d.mongodb.net/Library?retryWrites=true&w=majority".format(secret.username, secret.password))
new_user = {
  "_id": None,
  "loans":[],
  "name":"Donald J. Trump",
  "user":"abc",
  "phone":"+65-wewe"
}
create_user(client, new_user)