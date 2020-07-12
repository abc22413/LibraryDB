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
RENEW_DURATION = LOAN_DURATION

#Books
def gen_new_bookID(bookobj):
  #Generate new book ID in the format A00001ABC where ABC is first 3 letters of author's name
  bookobj["_id"] = str(random.randint(1,99999)).zfill(5)+bookobj["authors"][0].replace(" ","")[:3].upper()
  return bookobj

def create_book(client, new_book):
  #Add supplied new_book to DB
  new_book = gen_new_bookID(new_book)
  retry = 0
  #For around 6000 books, 41 retries ensures 1 in a billion chance of failure
  while retry<41:
    try:
      retry+=1
      success = client.Library.Books.insert_one(new_book).inserted_id
      print("Successfully added book with Book ID {0}".format(success))
      break
    except:
      #If insertion fails due to duplicate _id, try again
      new_book = gen_new_bookID(new_book)
      continue
    finally:
      input("Press Enter to continue")

def get_books(client, title, author, isbn, num_results, sort, direction):
  #Search for many books
  #List of fields that can be used for sorting
  sorting = ["_id","title", "author", "isbn", "pgs"]
  try:
    projection = {
      "_id":0,
      "title":1,
      "authors":1,
      "avail":1,
    }
    #Add # of pgs / isbn if using them to sort
    if sort==5:
      projection["pgs"]=1
    elif sort==4:
      projection["isbn"]=1
    #MongoDB query
    results = client.Library.Books.find({
      "title":{"$regex": title, "$options":"i"},
      "authors":{"$elemMatch": {"$regex": author, "$options": "i"}},
      "isbn":{"$regex": isbn}
    }, projection).limit(num_results).sort(sorting[sort-1], 1 if direction==1 else -1)
    #Print out data with ISBN/# of pgs as necessary
    print("Title | Author(s) | Available{0}".format(
      " | # of pages" if sort==5 else (" | ISBN" if sort==4 else "")
    ))
    for book in results:
      #Title | Author(s) | Availability | ISBN/# of pgs as necessary
      print("{0} | {1} | {2}{3}".format(
        #Title
        book["title"] if "title" in book.keys() else "No Title",
        #Author(s)
        ", ".join([i for i in book["authors"]]) if "authors" in book.keys() else "No Author(s)",
        #Availability
        "Available" if book["avail"] else "On Loan",
        #Optional ISBN/#of pages
        " | {0} pages".format(book["pgs"]) if sort==5 and "pgs" in book.keys() else 
        (" | "+book["isbn"] if sort==4 and "isbn" in book.keys() else "")
      ))

  except:
    print("Search failed")

  finally:
    input("Press Enter to continue")
  
def detail_books(client, title, author, isbn):
  #Get details of a (few) specific book(s)
  try:
    results = client.Library.Books.find({
      "title":{"$regex": title, "$options":"i"},
      "authors":{"$elemMatch": {"$regex": author, "$options": "i"}},
      "isbn":{"$regex": isbn}
    })
    #Dictionary of field name : string to display
    display = {
      "title":"\nTitle",
      "authors":"Written by",
      "avail":"Availability",
      "pgs":"Length",
      "isbn":"ISBN",
      "_id":"Book ID"
    }
    for book in results:
      #Handle books without certain fields
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
  #Retrieve 1 specific book and show its details
  try:
    book = client.Library.Books.find_one({"_id":book_id})
    #Dictionary of field name:string to display
    display = {
      "title":"\nTitle",
      "authors":"Author(s)",
      "pgs":"Length",
      "isbn":"ISBN",
      "_id":"Book ID"
    }
    #Handle books without certain fields
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
  #Update book in DB by replacing with new copy
  try:
    #Only insert if changes were made
    if old!=new:
      insert = {}
      for key in new.keys():
        #This allows for blank fields to be deleted, removing that attr from book
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
  #Delete a book in DB by _id
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
#TODO: Show overdue and prevent borrowing & renewal
def new_loan(client, user_id, book_id):
  #New loan object
  new_loan = {
    "book_id": book_id,
    "start": datetime.datetime.utcnow(),
    "due": datetime.datetime.utcnow()+LOAN_DURATION,
    "renew": False
  }
  try:
    user = client.Library.Users.find_one({"_id": user_id}, {"_id":0, "loan_num":1})
    #Check user does not have more than maximum loans
    if user["loan_num"]>=MAX_LOANS:
      print("User has too many loans")
      raise TooManyLoans
    #Check book being loaned is available for loan
    book = client.Library.Books.find_one({"_id":book_id}, {"_id":0, "avail":1})
    if not book["avail"]:
      print("Book not available for borrowing")
      raise BookNotAvail
    #Main update
    client.Library.Users.update_one({"_id": user_id}, {
      "$push":{
        "loans": new_loan
      },
      "$inc":{
        "loan_num": 1
      }
    })
    #Set borrowed book to unavailable
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
    print("\nUser ID: {0}".format(user["_id"]))
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
      print("\n{0}".format("OVERDUE" if datetime.datetime.utcnow()>loan["due"] else ""))
      print("Book ID: {0}".format(book["_id"]))
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
  try:
    loans = client.Library.Users.find_one({"_id": user_id}, {"_id":0, "loans":1})["loans"]
    #Get specific loan by searching with book_id
    [loan] = [i for i in loans if i["book_id"]==book_id]
    #Check loan has not been renewed yet
    if loan["renew"]==True:
      print("Book has already been renewed once")
      raise AlreadyRenewed
    #Add RENEW_DURATION to duedate
    loan["due"] += RENEW_DURATION
    loan["renew"]=True
    client.Library.Users.update_one(
      {"_id": user_id},
      {
        "$set": {"loans.$[element]": loan},
      },
      array_filters=[{"element.book_id": book_id}]
    )
    print("Succesfully renewed loan")
  except:
    print("Failed to renew loan")
  finally:
    input("Press Enter to continue")

def return_loan(client, user_id, book_id):
  try:
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
        "$pull": {"loans": {"book_id": book_id} },
        "$inc": {"loan_num": -1}
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
  except:
    print("Could not return loan")
  finally:
    input("Press Enter to continue")

def find_loaner(client, book_id):
  try:
    user = client.Library.Users.find_one({
      "loans":{"$elemMatch": {"book_id": book_id}}
    },{
      "loan_num":0,
      "loans":0
    })
    print("\nID of loaner: {0}".format(user["_id"]))
    print("Name: {0}".format(user["name"]))
    print("Username: {0}".format(user["user"]))
    print("Phone: {0}".format(user["phone"]))
  except:
    print("Could not find loaner of book {0}".format(book_id))
  finally:
    input("Press Enter to continue")

def past_loans(client, user_id):
  pass