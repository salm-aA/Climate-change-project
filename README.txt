SILVER SCREEN CINEMA BOOKING SYSTEM
===================================

Student name: [ENTER YOUR FULL NAME]
P-number: [ENTER YOUR P-NUMBER]
Course code: IY499
Repository: https://github.com/salm-aA/Climate-change-project

PROGRAM DESCRIPTION
-------------------
Silver Screen Cinema is a Python desktop application for browsing films and
booking cinema tickets. The Movies tab displays the title, genre, rating,
duration and price of each film. A customer can search by title or genre and
sort the results by title, genre, rating or price. After selecting a film, the
customer chooses a showtime, enters their name and books between one and ten
tickets. The program checks the number of seats available, calculates the total
price and creates a booking reference.

The Bookings tab displays saved reservations and allows a selected booking to
be cancelled. Cancelling returns the tickets to the available seat total. Movie
and booking information is read from and written to JSON files, so bookings are
still available after closing and reopening the application. The program uses
functions, loops, if statements, lists, dictionaries, arithmetic, recursion,
merge sort, binary search, file input/output, a Tkinter user interface and error
handling for invalid input or damaged files.

PACKAGES AND LIBRARIES
----------------------
No external packages are required. The program uses these Python standard
libraries: tkinter, json and os.

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
1. Search for a title or genre, or leave the search box empty to see all films.
2. Select a sorting option if required.
3. Select a movie from the table.
4. Enter a customer name, choose a showtime and enter the ticket quantity.
5. Select Confirm booking. The booking is saved in data/bookings.json.
6. Open the Bookings tab to view or cancel a reservation.

PROJECT FILES
-------------
main.py             User interface, validation, calculations and file access.
algorithms.py        Recursive searching and sorting algorithms.
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
