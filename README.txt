SILVER SCREEN CINEMA BOOKING SYSTEM
===================================

Student name: [ENTER YOUR FULL NAME]
P-number: [ENTER YOUR P-NUMBER]
Course code: IY499
Repository: https://github.com/salm-aA/Climate-change-project

PROGRAM DESCRIPTION
-------------------
Silver Screen Cinema is a Python menu-based application for browsing films and
booking cinema tickets. The main menu allows a customer to view every movie,
search by title or genre and sort the results by title, rating or price. To make
a booking, the customer selects a numbered movie and showtime, enters their
name and chooses between one and ten tickets. The program checks the number of
seats available, calculates the total price and creates a booking reference.

The customer can also view saved bookings or cancel one using its reference.
Cancelling returns the tickets to the available seat total. Movie and booking
information is read from and written to JSON files, so bookings are still
available after closing and reopening the application. The program uses
functions, loops, if statements, lists, dictionaries, arithmetic, recursion,
bubble sort, binary search, file input/output, a command-line user interface
and error handling for invalid input or damaged files.

PACKAGES AND LIBRARIES
----------------------
No external packages are required. The program uses these Python standard
libraries: json and os.

INSTALLATION
------------
1. Install Python 3.10 or later from https://www.python.org/downloads/
2. Download and unzip the project.
3. Open a terminal or command prompt in the project folder.
4. No pip installation is required because the program has no external
   packages.

HOW TO RUN THE PROGRAM
----------------------
Windows:
    python main.py

macOS or Linux:
    python3 main.py

HOW TO USE THE PROGRAM
----------------------
1. Enter a number from 1 to 7 at the main menu.
2. Use option 1 to view all films.
3. Use option 2 to search by title or genre.
4. Use option 3 to sort the films.
5. Use option 4 to choose a film and book tickets.
6. Use options 5 and 6 to view or cancel a reservation.

PROJECT FILES
-------------
main.py             Menu, booking, validation, calculations and file access.
algorithms.py        Bubble sort and recursive binary search algorithms.
data/movies.json     Movie, showtime, price and seat information.
data/bookings.json   Saved customer bookings.
requirements.txt     Confirms that no external packages are needed.
README.txt           Full project information required for submission.

DECLARATION OF OWN WORK
-----------------------
I confirm that this assignment is my own work.

Where I have referred to online sources, I have provided comments detailing the
reference and included a link to the source.

IMPORTANT: Replace the name and P-number placeholders before submission. Only
include the declaration if it is accurate under your university's rules on AI
and other assistance.
