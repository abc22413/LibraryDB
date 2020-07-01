from dbhandler import *
from datetime import datetime

def show_welcome():
  print("\n\n\nWELCOME TO ABC LIBRARY")
  print("Current Time {0}".format(datetime.now().strftime("%d %B %Y %H:%M:%S")))

def show_menu(options):
  print("\n\n\nChoose an option below")
  for x in options:
    print("{0}) {1}".format(
      options.index(x)+1,
      x
      )
    )
  while True:
    try:
      option = int(input("Option: "))
      if option not in [i for i in range(1,len(options)+1)]:
        #raise RangeError
        pass
    except ValueError:
      print("Not an integer selection. Please try again")
      continue
    if option not in [i for i in range(1,len(options)+1)]:
      print("Selection out of range. Please try again")
      continue
    else:
      break
  return option

def start_cli():
  show_welcome()
  while True:
    main_option=show_menu([
      "Quit",
      "Manage Account & Loans",
      "Browse Books",
      "Administer Library"
    ])

    #Choose to quit
    if main_option==1:
      break

    #Choose to account manage
    elif main_option==2:
      while True:
        acc_option=show_menu([
          "Return to previous",
          "Borrow Book",
          "Return Book"
        ])
        
        #Return to above
        if acc_option==1:
          break

        #Borrow book
        elif acc_option==2:
          while True:
            bor_option=show_menu([
              "Return to previous",
              "Borrow another Book"
            ])

            #Return to above
            if bor_option==1:
              break

            #Borrow a book
            elif bor_option==2:
              pass

        #Return book
        elif acc_option==3:
          while True:
            ret_option=show_menu([
              "Return to previous",
              "Return another Book"
            ])

            #Return to above
            if ret_option==1:
              break

            #Borrow a book
            elif ret_option==2:
              pass
  
    #Choose to browse
    elif main_option==3:
      pass

    #Choose to administer library
    elif main_option==4:
      pass

  #End of program
  print("Thank you for visiting ABC Libary")
  print("Session ended {}".format(datetime.now().strftime("%d %B %Y %H:%M:%S")))