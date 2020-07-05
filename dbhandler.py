#Handle MongoDB backend queries, searches, sorts
import dns
import errors
import secret
import random
from pymongo import *

def gen_new_bookID(bookobj):
  bookobj["_id"] = str(random.randint(1,99999)).zfill(5)+bookobj["authors"][0].replace(" ","")[:3].upper()
  return bookobj

#Books
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
    input("\nPress Enter to continue")

def get_one_book(client, book_id):
  try:
    book = client.Library.Books.find_one({"_id":book_id})
    print("\nTitle: {}".format(book["title"]))
    print("Author(s): {}".format(", ".join([i for i in book["authors"]])))
    print("Length: {} pages".format(book["pgs"]))
    print("ISBN: {}".format(book["isbn"]))
    print("Book ID: {}".format(book["_id"]))
    input("Press Enter to continue\n")
    return book
  except:
    print("Failed to retrieve such book")
    return None

def update_book(client, old, new):
  try:
    if old!=new:
      client.Library.Books.find_one_and_replace({"_id":new["_id"]},new)
      print("Successfully modified")
    else:
      print("No modifications done.")
  except:
    print("Error occurred while attempting to modify")

def delete_book(client, del_id):
  client, del_id = client, del_id
  try:
    client.delete_one({

    })

  except:
    print("Failed to delete")

  finally:
    input("Press Enter to continue")

#Users
def create_user(client):
  pass

def get_users(client):
  pass

def update_user(client):
  pass

def delete_user(client):
  pass

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