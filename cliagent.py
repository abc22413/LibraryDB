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

def get_param(options, command="\nPlease supply the following"):
  results=[]
  for option in options.keys():
    while True:
      if options[option]==str:
        try:
          temp = str(input("{}: ".format(option)))
          results.append(temp)
          break
        except:
          if temp=='':
            results.append(temp)
            break
          else:
            print("Please input a string for {}".format(option))
      elif options[option]==int:
        try:
          temp = int(input("{}: ".format(option)))
          results.append(temp)
          break
        except:
          if temp=='':
            results.append(None)
            break
          else:
            print("Please input an integer for {}".format(option))
  return results

def start_cli(client):
  #Supplies mongodb client
  client = client

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
          "New search",
          "View book details"
        ])

        #Return
        if option==1:
          break

        #New Search
        elif option==2:
          [title, author, isbn, num_results] = get_param({
            "Title":str,
            "Author":str,
            "ISBN":str,
            "Number of results":int,
          },"\nNew search")
          num_results = num_results if num_results else 10
          sort = show_menu([
            "None",
            "Title",
            "Author",
            "ISBN",
            "Number of Pages"
          ],"\nSort by")
          direction=1
          if sort!=1:
            direction = show_menu([
              "Ascending",
              "Descending"
            ], "\nSort in which direction")
          get_books(client, title, author, isbn, num_results, sort, direction)

        elif option==3:
          [title, author, isbn] = get_param({
            "Title":str,
            "Author":str,
            "ISBN":str
          },"\nFind book details")
          detail_books(client, title, author, isbn)

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
          "Borrow Book",
          "Renew Book",
          "Return Book",
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
          [title, isbn, pgs] = get_param({
            "Title":str,
            "ISBN":str,
            "# of pages":int
          }, "Supply the following")
          authors=[]
          author_count=1
          while True:
            authors.append(input("Author {}: ".format(author_count)))
            if str(input("Add another author? (y/n) ")).lower() not in ["y","yes","yeah","sure","yep","yup"]:
              break
            author_count+=1
          new_book = {
            "_id": None,
            "title": title,
            "authors": authors,
            "avail": True,
            "pgs": pgs,
            "isbn": isbn
          }
          try:
            create_book(client, new_book)
          except:
            print("Creation failed")
          finally:
            input("Press Enter to continue")

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