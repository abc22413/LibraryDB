#Handle MongoDB backend queries, searches, sorts
import dns
import errors
import secret
import random
import string
from pymongo import *

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
    for book in results:
      print("{0} | {1} | {2}{3}".format(
        book["title"],
        ", ".join([i for i in book["authors"]]),
        "Available" if book["avail"] else "On Loan",
        " | {0} pages".format(book["pgs"]) if sort==5 else (" | "+book["isbn"] if sort==4 else "")
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
    for book in results:
      print("\nTitle: {}".format(book["title"]))
      print("Written by: {}".format(", ".join([i for i in book["authors"]])))
      print("Availability: {}".format("Available" if book["avail"] else "On Loan"))
      print("Length: {} pages".format(book["pgs"]))
      print("ISBN: {}".format(book["isbn"]))
      print("Book ID: {}".format(book["_id"]))

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
        if new[key] not in ['', None, []]:
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
    for user in results:
      print("{0} | {1} | {2}".format(
        user["name"],
        user["user"],
        user["phone"]
      ))

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
def new_loan(client):
  pass

def cur_loans(client):
  pass

def renew_loan(client):
  pass

def return_loan(client):
  pass

def past_loans(client):
  pass