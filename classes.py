from dbhandler import *

class Book:
  def __init__(self, ):
    self.id = None
    self.title = ""
    self.isbn = ""
    self.authors = []
    self.pgs = 0
    self.avail = True

  def list_view(self):
    print(self.title)

class User:
  def __init__(self):
    self.id = None
    self.name = ""
    self.username = ""
    self.phone = ""

class Loan:
  def __init__(self):
    self.user = None
    self.book = None
    self.start = None