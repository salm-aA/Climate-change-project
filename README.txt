SILVER SCREEN CINEMA BOOKING SYSTEM
===================================

Student name: [ENTER YOUR FULL NAME]
P-number: [ENTER YOUR P-NUMBER]
Course code: IY499
Online repository: https://github.com/salm-aA/Climate-change-project

DESCRIPTION
-----------
Silver Screen Cinema is a Python desktop application for browsing films and
booking cinema tickets. The Movies and Booking screen displays each film's
genre, audience rating, duration, ticket price and available showtimes. A user
can search by title or genre and sort the results by title, genre, rating or
price. After selecting a film, the user enters their name, chooses a showtime
and reserves between one and ten tickets. The program checks the remaining
capacity, calculates the total price and creates a unique booking reference.

The Manage Bookings screen displays all saved reservations and allows a user
to cancel one. Cancelling restores the seats to the relevant showing. Movie,
showtime and booking information is stored in JSON files, so changes remain
available after the application closes. The project demonstrates functions,
nested lists and dictionaries, file input/output, a recursive binary search,
recursive merge sort, a Tkinter interface and error handling for invalid input,
missing records, unavailable seats and damaged files.

PACKAGES AND LIBRARIES
----------------------
No external packages are required. The program uses Python standard-library
modules: tkinter, json, pathlib, tempfile, os, datetime and uuid.

INSTALLATION
------------
1. Install Python 3.10 or later from https://www.python.org/downloads/
2. Download and unzip this project.
3. Open a terminal or command prompt inside the cinema_booking_app folder.
4. No pip installation is needed because requirements.txt has no dependencies.

RUNNING THE PROGRAM
-------------------
Windows:
    python main.py

macOS or Linux:
    python3 main.py

Select a movie row, choose a showtime, enter a customer name and ticket count,
then press Confirm booking. Use the Manage bookings tab to view or cancel saved
bookings.

RUNNING THE TESTS
-----------------
From the cinema_booking_app folder, run:

Windows:
    python -m unittest discover -s tests -v

macOS or Linux:
    python3 -m unittest discover -s tests -v

FILES
-----
main.py              Starts the application.
ui.py                Creates the graphical user interface.
cinema.py            Contains booking and cinema business logic.
algorithms.py         Contains searching and sorting algorithms.
validation.py         Checks customer names and ticket counts.
storage.py            Reads and safely writes JSON data.
data/movies.json      Stores films, showtimes and seat availability.
data/bookings.json    Stores confirmed bookings.
tests/test_cinema.py  Tests important functionality and error cases.

GITHUB / VERSION CONTROL
------------------------
Create your own online repository and make small commits as you develop and
understand the project. Examples of clear commit messages are:
    Add movie JSON data and file loading
    Implement recursive searching and sorting
    Add ticket booking validation
    Build Tkinter movie browser
    Add booking cancellation and automated tests
    Complete README instructions

Do not upload passwords, personal data or your Python cache folders.

DECLARATION OF OWN WORK
-----------------------
I confirm that this assignment is my own work.

Where I have referred to online sources, I have provided comments detailing the
reference and included a link to the source.

Before submission, replace every [ENTER ...] placeholder above and make sure the
README accurately describes the version you submit.
