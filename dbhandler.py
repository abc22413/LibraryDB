import dns
import secret
from pymongo import *

#Books
def create_book(client):
  pass

def get_books(client, title, author, isbn, num_results=10):
  collection = client.Library.Books
  return collection.find({"title": {"$regex": title}},{"_id":0, "pgs":0, "isbn": 0}).limit(num_results)

def update_book(client):
  pass

def delete_book(client):
  pass

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

print(get_books("", "", ""))