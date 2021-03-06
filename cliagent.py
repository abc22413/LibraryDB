#Handle Front and middle of application: CLI and processing
from errors import *
from dbhandler import *
from datetime import datetime
import time
import copy

#Responses which indicate yes for "y/n" prompts
AFFIRMATIVE = ["y","yes","yeah","yah","yep","yup","ye","ya",""]

def show_welcome():
  #Show welcome message
  print("\n\n\nWELCOME TO ABC LIBRARY")
  print("Current Time {0}".format(datetime.now().strftime("%d %B %Y %H:%M:%S")))

def show_menu(options, command="\n\n\nChoose an option below"):
  #Show a menu with options specified by options
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
      #If selected option is out of range shown by the menu
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
  #Show prompt to get values for variables specified in options
  results=[]
  print(command)
  for option in options.keys():
    while True:
      #If variable is str type
      if options[option]==str:
        try:
          #temp is temporary variable for storing response
          temp=""
          temp = str(input("{}: ".format(option)))
          results.append(temp)
          break
        except:
          #Accept blank responses
          if temp=="":
            results.append(temp)
            break
          #Handle exception not related to response
          else:
            print("Please input a string for {}".format(option))
      #For int type variable
      elif options[option]==int:
        try:
          #temp is temporary variable to store response
          temp = None
          temp = int(input("{}: ".format(option)))
          results.append(temp)
          break
        except:
          #Accept blank response
          if temp==None:
            results.append(None)
            break
          #Handle exception not related to blank response
          else:
            print("Please input an integer for {}".format(option))
  return results

def start_cli(client):
  #Supplies mongodb client
  client = client

  #mainloop
  while True:
    #Main option in program
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

        #Details View
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
          [user_id] = get_param({"User ID":str}, "\nSupply user ID")
          cur_loans(client, user_id)
          
        #Past Loans
        elif option==3:
          [user_id, num_results] = get_param({
            "User ID":str,
            "Number of results":int
          })
          if not num_results:
            num_results=20
          past_loans(client, user_id, num_results)

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
          #Enter user_id
          [user_id] = get_param({
                "Your user ID":str,
              }, "\nSupply your user ID")
          while True:
            #True loop allows multiple books to be borrowed without keying in user_id every time
            borrow_option = show_menu([
              "Return to previous",
              "Borrow a(nother) book"
            ])
            if borrow_option==1:
              break
            elif borrow_option==2:
              [book_id] = get_param({
                "Book ID to borrow":str
              }, "\nSupply the book ID of the book you wish to borrow")
              new_loan(client, user_id, book_id)

        #Renew Book(s)
        elif option==3:
          [user_id] = get_param({
            "User ID":str
          }, "\nSupply your user ID")
          books = cur_loans(client, user_id, True)
          #Handle if no books were returned
          if not books:
            print("No current loans were returned. Have you borrowed anything yet?")
            continue
          #Choose which book to renew if at all
          while True:
            renew_option = show_menu([
              "Return to previous",
            ]+["Renew "+book["title"] for book in books])
            if renew_option==1:
              break
            elif renew_option in range(2,2+len(books)):
              renew_loan(client, user_id, books[renew_option-2]["_id"])

        #Return Book(s)
        elif option==4:
          [user_id] = get_param({
            "User ID":str
          }, "\nSupply your user ID")
          books = cur_loans(client, user_id, True)
          #Handle if no books were returned
          if not books:
            print("No current loans were returned. Have you borrowed anything yet?")
            continue
          #Choose which book to return if at all
          while True:
            return_option = show_menu([
              "Return to previous",
            ]+["Return "+book["title"] for book in books])
            if return_option==1:
              break
            elif return_option in range(2,2+len(books)):
              if return_loan(client, user_id, books[return_option-2]["_id"]):
                books = [i for i in books if i!=books[return_option-2]]

        #Check book loaner
        elif option==5:
          [book_id] = get_param({
            "Book ID":str
          }, "\nSupply ID of book you wish to investigate")
          find_loaner(client, book_id)

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
            if str(input("Add another author? (y/n) ")).lower() not in AFFIRMATIVE:
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
          create_book(client, new_book)

        #Edit book
        elif option==3:
          [book_id]=get_param({"Book ID":str},"\nSupply Book ID")
          book = get_one_book(client, book_id)
          if book==None:
            continue
          #Create local editing copy
          new_book = copy.deepcopy(book)
          while True:
            edit_option=show_menu([
              "Discard changes & Return",
              "Commit changes & Return",
              "Edit Title",
              "Edit #of pages",
              "Edit ISBN",
              "Edit Author(s)"
            ])
            #Discard changes
            if edit_option==1:
              print("Exiting editor mode")
              break

            #Commit changes
            elif edit_option==2:
              update_book(client, book, new_book)
              print("Exiting editor mode")
              break
            
            elif edit_option in range(3,6):
              editing = ["title", "pgs", "isbn"]
              field = editing[edit_option-3]
              try:
                #Check attr exists
                if field not in new_book.keys():
                  new_book[field] = None if field=="pgs" else ''
                [response] = get_param({"New {}".format(field):int if field=="pgs" else str}, "\nSupply new {0}".format(field))
                if str(input("Confirm changing {0} from '{1}' to '{2}'? (y/n): ".format(
                  field,
                  new_book[field],
                  response
                ))).lower() in AFFIRMATIVE:
                  new_book[field] = response
                
              finally:
                input("Press Enter to continue")

            elif edit_option==6:
              try:
                if "authors" not in new_book.keys():
                  new_book["authors"]=["New Author"]
                new_authors = copy.deepcopy(new_book["authors"])
                while True:
                  author_option = show_menu(["Discard changes & Return", "Commit changes & Return"]+new_authors, "\nChoose author to edit")
                  #Discard and Return
                  if author_option==1:
                    break

                  #Commit and Return
                  elif author_option==2:
                    new_book["authors"]=new_authors
                    print("Successfully added modifications to local copy")
                    break

                  #Change an author
                  elif author_option in range(3, len(new_authors)+3):
                    author = new_authors[author_option-3]
                    while True:
                      new_author = str(input("Replace {} with: ".format(author)))
                      if str(input("Confirm changing '{0}' to '{1}'? (y/n): ".format(
                        author,
                        new_author
                      ))).lower() in AFFIRMATIVE:
                        if new_author!='':
                          new_authors[author_option-3] = new_author
                        else:
                          new_authors.pop(author_option-3)
                        break    
                
              finally:
                input("Press Enter to continue")

        #Remove book
        elif option==4:
          [book_id]=get_param({"Book ID":str},"\nSupply Book ID")
          delete_book(client, book_id)

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
          [name, user, phone] = get_param({
            "Real Name":str,
            "Username":str,
            "Phone Number":str
          }, "\nPlease enter user credentials")
          new_user = {
            "_id": None,
            "loan_num": 0,
            "loans":[],
            "name":name,
            "user":user,
            "phone":phone
          }
          create_user(client, new_user)

        #Edit user
        elif option==3:
          [user_id]=get_param({"User ID":str},"\nSupply User ID")
          user = get_one_user(client, user_id)
          if user==None:
            continue
          #Create local editing copy
          new_user = copy.deepcopy(user)
          while True:
            edit_option=show_menu([
              "Discard changes & Return",
              "Commit changes & Return",
              "Edit Name",
              "Edit Username",
              "Edit Phone",
            ])
            #Discard changes
            if edit_option==1:
              print("Exiting editor mode")
              break

            #Commit changes
            elif edit_option==2:
              update_user(client, user, new_user)
              print("Exiting editor mode")
              break
            
            elif edit_option in range(3,6):
              editing = ["name", "username", "phone"]
              fields = ["name", "user", "phone"]
              edit_field = editing[edit_option-3]
              field = fields[edit_option-3]
              try:
                if field not in new_user.keys():
                  new_user[field]=''
                [response] = get_param({"New {}".format(edit_field):str}, "\nSupply new {0}".format(edit_field))
                if str(input("Confirm changing {0} from '{1}' to '{2}'? (y/n): ".format(
                  edit_field,
                  new_user[field],
                  response
                ))).lower() in AFFIRMATIVE:
                  new_user[field] = response
                  print("Successfully edited field of user")

              finally:
                input("Press Enter to continue")

        #Search users
        elif option==4:
          [name, username, num_results] = get_param({
            "Name":str,
            "Username":str,
            "Number of results":int,
          },"\nNew search")
          num_results = num_results if num_results else 10
          sort = show_menu([
            "None",
            "Name",
            "Username",
          ],"\nSort by")
          direction=1
          if sort!=1:
            direction = show_menu([
              "Ascending",
              "Descending"
            ], "\nSort in which direction")
          get_users(client, name, username, num_results, sort, direction)

        #Remove user
        elif option==5:
          [user_id]=get_param({"User ID":str},"\nSupply User ID")
          delete_user(client, user_id)