import dns
import secret
from pymongo import *

#Books
def create_book(client, new_book):
  client, new_book = client, new_book
  try:
    new_id = client.Library.Books.insert_one(new_book).inserted_id
    print("Success! {0} was added with ID {1}".format(new_book["title"], new_id))
  except:
    print("Failed to insert book")
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
      print("Library ID: {}".format(book["_id"]))

    print("\nPlease take note of Library ID for borrowing")

  except:
    print("Details search failed")

  finally:
    input("\nPress Enter to continue")

def update_book(client):
  pass

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