from classes import *
from errors import *
from dbhandler import *
from datetime import datetime
import time

def show_welcome():
  print("\n\n\nWELCOME TO ABC LIBRARY")
  print("Current Time {0}".format(datetime.now().strftime("%d %B %Y %H:%M:%S")))

def show_menu(options, command="\n\n\nChoose an option below"):
  print(command)
  for x in options:
    print("{0}) {1}".format(
      options.index(x)+1,
      x
      )
    )
  #Loop to ensure proper input handling
  while True:
    try:
      option = int(input("Option: "))
      #If selected option out of range shown by the menu
      if option not in [i for i in range(1,len(options)+1)]:
        raise OptionOutOfRange
      break
    except ValueError:
      print("Not an integer selection. Please try again")
      continue
    except OptionOutOfRange:
      print("Selection out of range. Please try again")
      continue
  return option

def get_search_param():
  print("\nNew Search")
  title = str(input("Title: "))
  author = str(input("Author: "))
  isbn = str(input("ISBN: "))

  #Handle integer input gathering
  while True:
    try:
      num_results = int(input("How many results to display? "))
      break
    except TypeError:
      if num_results=="":
        num_results = None
        break
      print("Please enter integer value")

  return title, author, isbn, num_results

def start_cli(client):
  #Supplies mongodb client
  client = client
  show_welcome()
  time.sleep(2)

  #mainloop
  while True:
    main_option = show_menu([
      "Quit",
      "Browse Books",
      "Check Loans",
      "Manage Loans",
      "Manage Books",
      "Manage Users"
    ])

    #Choose to quit
    if main_option==1:
      break

    #Browse Books
    elif main_option==2:
      while True:
        option = show_menu([
          "Return to previous",
          "New search"
        ])

        #Return
        if option==1:
          break

        #New Search
        elif option==2:
          search_start = time.time()
          title, author, isbn, num_results = get_search_param()
          if num_results:
            results = get_books(client, title, author, isbn, num_results)
          else:
            results = get_books(client, title, author, isbn, num_results)
          #Print results
          print("{0} results in {1}ms".format(
            len(results),
            time.time()-search_start
          ))
          print("Title | Author(s) | Availability")
          for book in results:
            print("{0} | {1} | {2}".format(
              book["title"],
              book["authors"],
              book["avail"]
            ))

    #Check Loans
    elif main_option==3:
      while True:
        option = show_menu([
          "Return to previous",
          "Check current loans",
          "Check past loans"
        ])

        #Return
        if option==1:
          break

        #Current Loans
        elif option==2:
          pass

        #Past Loans
        elif option==3:
          pass

    #Manage Loans
    elif main_option==4:
      while True:
        option = show_menu([
          "Return to previous",
          "Borrow Book(s)",
          "Renew Book(s)",
          "Return Book(s)",
          "Check book loaner",
        ])

        #Return
        if option==1:
          break

        #Borrow Book(s)
        elif option==2:
          pass

        #Renew Book(s)
        elif option==3:
          pass

        #Return Book(s)
        elif option==4:
          pass

        #Check book loaner
        elif option==5:
          pass

    #Manage Books
    elif main_option==5:
      while True:
        option = show_menu([
          "Return to previous",
          "Add book",
          "Edit book",
          "Remove book"
        ])

        #Return
        if option==1:
          break

        #Add book
        elif option==2:
          pass

        #Edit book
        elif option==3:
          pass

        #Remove book
        elif option==4:
          pass

    #Manage Users
    elif main_option==6:
      while True:
        option = show_menu([
          "Return to previous",
          "Add user",
          "Edit user",
          "Search users",
          "Remove user"
        ])

        #Return
        if option==1:
          break

        #Add user
        elif option==2:
          pass

        #Edit user
        elif option==3:
          pass

        #Search users
        elif option==4:
          pass

        #Remove user
        elif option==5:
          pass

  #End of program
  print("\nThank you for visiting ABC Libary")
  print("Session ended {}".format(datetime.now().strftime("%d %B %Y %H:%M:%S")))