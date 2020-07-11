#Handle MongoDB backend queries, searches, sorts
import dns
import errors
import secret
import random
import string
import datetime
from pymongo import *
from errors import *

#Global variables
LOAN_DURATION = datetime.timedelta(days=27)
MAX_LOANS = 7
RENEW_DURATION = 0

#Books
def gen_new_bookID(bookobj):
  bookobj["_id"] = str(random.randint(1,99999)).zfill(5)+bookobj["authors"][0].replace(" ","")[:3].upper()
  return bookobj

def create_book(client, new_book):
  retry = 0
  new_book = gen_new_bookID(new_book)
  #For around 6000 books, 41 ensures 1 in a billion chance of failure
  while retry<41:
    try:
      retry+=1
      success = client.Library.Books.insert_one(new_book).inserted_id
      print("Successfully added book with Book ID {0}".format(success))
      break
    except:
      new_book = gen_new_bookID(new_book)
      continue
    finally:
      input("Press Enter to continue")

def get_books(client, title, author, isbn, num_results, sort, direction):
  sorting = ["_id","title", "author", "isbn", "pgs"]
  try:
    projection = {
      "_id":0,
      "title":1,
      "authors":1,
      "avail":1,
    }
    if sort==5:
      projection["pgs"]=1
    elif sort==4:
      projection["isbn"]=1
    results = client.Library.Books.find({
      "title":{"$regex": title, "$options":"i"},
      "authors":{"$elemMatch": {"$regex": author, "$options": "i"}},
      "isbn":{"$regex": isbn}
    }, projection).limit(num_results).sort(sorting[sort-1], 1 if direction==1 else -1)
    print("Title | Author(s) | Available{0}".format(
      " | # of pages" if sort==5 else (" | ISBN" if sort==4 else "")
    ))
    '''
    '''
    for book in results:
      print("{0} | {1} | {2}{3}".format(
        book["title"] if "title" in book.keys() else "No Title",
        ", ".join([i for i in book["authors"]]) if "authors" in book.keys() else "No Author(s)",
        "Available" if book["avail"] else "On Loan",
        " | {0} pages".format(book["pgs"]) if sort==5 and "pgs" in book.keys() else (" | "+book["isbn"] if sort==4 and "isbn" in book.keys() else "")
      ))

  except:
    print("Search failed")

  finally:
    input("Press Enter to continue")
  
def detail_books(client, title, author, isbn):
  try:
    results = client.Library.Books.find({
      "title":{"$regex": title, "$options":"i"},
      "authors":{"$elemMatch": {"$regex": author, "$options": "i"}},
      "isbn":{"$regex": isbn}
    })
    display = {
      "title":"\nTitle",
      "authors":"Written by",
      "avail":"Availability",
      "pgs":"Length",
      "isbn":"ISBN",
      "_id":"Book ID"
    }
    for book in results:
      for field in [i for i in display.keys() if i in book.keys()]:
        if field=="authors":
          print("Written by: {}".format(", ".join([i for i in book["authors"]])))
        elif field=="avail":
          print("Availability: {}".format("Available" if book["avail"] else "On Loan"))
        else:
          print("{0}: {1}".format(display[field], book[field]))
    print("\nPlease take note of Book ID for borrowing")

  except:
    print("Details search failed")

  finally:
    input("Press Enter to continue")

def get_one_book(client, book_id):
  try:
    book = client.Library.Books.find_one({"_id":book_id})
    display = {
      "title":"\nTitle",
      "authors":"Author(s)",
      "pgs":"Length",
      "isbn":"ISBN",
      "_id":"Book ID"
    }
    for field in [i for i in display.keys() if i in book.keys()]:
      if field=="authors":
        print("{0}: {1}".format(display[field], ", ".join([i for i in book[field]])))
      else:
        print("{0}: {1}".format(display[field], book[field]))
  except:
    print("Failed to retrieve such book")
  finally:
    input("Press Enter to continue")
    return book

def update_book(client, old, new):
  try:
    if old!=new:
      #remove attribute functionalty
      insert = {}
      for key in new.keys():
        if new[key] not in ['', None]:
          insert[key] = new[key]
      client.Library.Books.find_one_and_replace({"_id":insert["_id"]},insert)
      print("Successfully modified")
    else:
      print("No modifications done.")
  except:
    print("Error occurred while attempting to modify")
  finally:
    input("Press Enter to continue")

def delete_book(client, del_id):
  try:
    client.Library.Books.delete_one({"_id":del_id})
    print("Successfully deleted book with book ID {}".format(del_id))

  except:
    print("Failed to delete book with book ID {}".format(del_id))

  finally:
    input("Press Enter to continue")

#Users
def gen_new_userID(userobj):
  #(random Letter)99999ABC
  name=userobj["name"].replace(" ","")
  name="".join([i for i in name if i not in [",./';- "]]).upper()
  userobj["_id"] = random.choice(string.ascii_uppercase)+str(random.randint(1,99999)).zfill(5)+name[:3]
  return userobj

def create_user(client, new_user):
  new_user = gen_new_userID(new_user)
  try:
    success = client.Library.Users.insert_one(new_user).inserted_id
    print("Successfully added user with User ID {0}".format(success))
  except:
    print("Failed to make new user")
  finally:
    input("Press Enter to continue")

def get_users(client, name, username, num_results, sort, direction):
  sorting = ["_id","name","user"]
  try:
    results = client.Library.Users.find({
      "name":{"$regex": name, "$options":"i"},
      "user":{"$regex": username, "$options":"i"}
    },{"loans":0}).limit(num_results).sort(sorting[sort-1], 1 if direction==1 else -1)
    print("Name | Username | Phone")
    display = ["name", "user", "phone"]
    for user in results:
      to_print=""
      for field in [i for i in display if i in user.keys()]:
        to_print+=str(user[field])
        to_print+=" | "
      print(to_print)

  except:
    print("Search failed")

  finally:
    input("Press Enter to continue")

def get_one_user(client, user_id):
  try:
    user = client.Library.Users.find_one({"_id":user_id})
    display = {
      "name":"Name",
      "user":"Username",
      "phone":"Phone"
    }
    for field in [i for i in display.keys() if i in user.keys()]:
      print("{0}: {1}".format(display[field], user[field]))

  except:
    print("Failed to retrieve such user")
  finally:
    input("Press Enter to continue")
    return user

def update_user(client, old, new):
  try:
    if old!=new:
      #Remove attributes functionality
      insert = {}
      for key in new.keys():
        if new[key] not in ['', None]:
          insert[key] = new[key]
      client.Library.Users.find_one_and_replace({"_id":insert["_id"]},insert)
      print("Successfully modified")
    else:
      print("No modifications done.")
  except:
    print("Error occurred while attempting to modify")
  finally:
    input("Press Enter to continue")

def delete_user(client, del_id):
  try:
    client.Library.Users.delete_one({"_id":del_id})
    print("Successfully deleted user with User ID {}".format(del_id))

  except:
    print("Failed to delete user with User ID {}".format(del_id))

  finally:
    input("Press Enter to continue")

#Loans
def new_loan(client, user_id, book_id):
  new_loan = {
    "book_id": book_id,
    "start": datetime.datetime.utcnow(),
    "due": datetime.datetime.utcnow()+LOAN_DURATION,
    "renew": False
  }
  try:
    user = client.Library.Users.find_one({"_id": user_id}, {"_id":0, "loan_num":1})
    if user["loan_num"]>=MAX_LOANS:
      print("User has too many loans")
      raise TooManyLoans
    book = client.Library.Books.find_one({"_id":book_id}, {"_id":0, "avail":1})
    if not book["avail"]:
      print("Book not available for borrowing")
      raise BookNotAvail
    client.Library.Users.update_one({"_id": user_id}, {
      "$push":{
        "loans": new_loan
      },
      "$inc":{
        "loan_num": 1
      }
    })
    client.Library.Books.update_one({"_id": book_id}, {
      "$set":{
        "avail":False
      }
    })
    print("Succesfully borrowed book")
  except:
    print("Failed to process book borrowing")
  finally:
    input("Press Enter to continue")
#TODO:
def cur_loans(client, user_id, to_return=False):
  try:
    user = client.Library.Users.find_one({"_id":user_id}, {
      "_id":1,
      "name":1,
      "loans":1
    })
    print("User ID: {0}".format(user["_id"]))
    if "name" in user.keys():
      print("Name: {0}".format(user["name"]))
    #Only if to return
    if to_return:
      return_obj=[]
    for loan in user["loans"]:
      book = client.Library.Books.find_one({"_id": loan["book_id"]}, {
        "_id":1,
        "title":1,
      })
      print("\nBook ID: {0}".format(book["_id"]))
      print("Title: {0}".format(book["title"] if "title" in book.keys() else "No Title"))
      print("Date issued: {0}".format(loan["start"]))
      print("Due Date: {0}".format(loan["due"]))
      print("Renewed" if loan["renew"] else "Not Renewed")

      if to_return:
        return_obj.append(book)

    if to_return:
      return return_obj
    
  except:
    print("Failed to retrieve current loans")
  finally:
    input("Press Enter to continue")

def renew_loan(client, user_id, book_id):
  print("LOAN RENEWAL")

def return_loan(client):
  pass

def past_loans(client, user_id):
  pass