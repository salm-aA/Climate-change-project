"""A simple menu-based cinema ticket booking program."""

import json
import os

from algorithms import bubble_sort, search_movies


FOLDER = os.path.dirname(os.path.abspath(__file__))
MOVIES_FILE = os.path.join(FOLDER, "data", "movies.json")
BOOKINGS_FILE = os.path.join(FOLDER, "data", "bookings.json")


def load_file(filename):
    """Load a list from a JSON file."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print("Error: a data file could not be found.")
    except json.JSONDecodeError:
        print("Error: a data file is damaged.")
    except OSError:
        print("Error: a data file could not be opened.")
    return None


def save_file(filename, data):
    """Save a list to a JSON file."""
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)
        return True
    except OSError:
        print("Error: the data could not be saved.")
        return False


def display_movies(movie_list):
    """Print a numbered list of movies."""
    if len(movie_list) == 0:
        print("\nNo movies were found.")
        return

    print("\nAVAILABLE MOVIES")
    print("-" * 70)
    for number, movie in enumerate(movie_list, start=1):
        print(
            f"{number}. {movie['title']} | {movie['genre']} | "
            f"Rating: {movie['rating']} | £{movie['price']:.2f}"
        )
    print("-" * 70)


def view_all_movies(movies):
    """Display every movie."""
    display_movies(movies)


def search_for_movie(movies):
    """Ask for search text and display matching movies."""
    search_text = input("Enter a title or genre: ").strip()
    if search_text == "":
        print("Search text cannot be empty.")
        return
    results = search_movies(movies, search_text)
    display_movies(results)


def sort_movies(movies):
    """Sort and display movies using bubble sort."""
    print("\n1. Sort by title")
    print("2. Sort by rating")
    print("3. Sort by price")
    choice = input("Choose an option: ").strip()

    fields = {"1": "title", "2": "rating", "3": "price"}
    if choice not in fields:
        print("Invalid sorting option.")
        return

    sorted_movies = bubble_sort(movies, fields[choice])
    display_movies(sorted_movies)


def choose_number(question, minimum, maximum):
    """Keep asking until the user enters a valid whole number."""
    while True:
        try:
            number = int(input(question))
            if minimum <= number <= maximum:
                return number
            print(f"Enter a number between {minimum} and {maximum}.")
        except ValueError:
            print("Please enter a whole number.")


def next_booking_id(bookings):
    """Create a simple booking reference."""
    highest_number = 0
    for booking in bookings:
        try:
            number = int(booking["id"].replace("B", ""))
            if number > highest_number:
                highest_number = number
        except (KeyError, ValueError):
            pass
    return f"B{highest_number + 1:03d}"


def book_tickets(movies, bookings):
    """Create and save a cinema booking."""
    display_movies(movies)
    movie_number = choose_number("Choose a movie number: ", 1, len(movies))
    movie = movies[movie_number - 1]

    print(f"\nSHOWTIMES FOR {movie['title'].upper()}")
    for number, showing in enumerate(movie["showtimes"], start=1):
        seats_left = showing["capacity"] - showing["booked"]
        print(f"{number}. {showing['time']} ({seats_left} seats left)")

    time_number = choose_number("Choose a showtime number: ", 1, len(movie["showtimes"]))
    showing = movie["showtimes"][time_number - 1]
    seats_left = showing["capacity"] - showing["booked"]

    if seats_left == 0:
        print("Sorry, this showing is full.")
        return

    customer_name = input("Enter customer name: ").strip()
    if len(customer_name) < 2:
        print("The name must contain at least two characters.")
        return

    maximum_tickets = min(10, seats_left)
    ticket_number = choose_number(
        f"Number of tickets (1-{maximum_tickets}): ", 1, maximum_tickets
    )
    total_price = round(movie["price"] * ticket_number, 2)

    booking = {
        "id": next_booking_id(bookings),
        "customer": customer_name,
        "movie_id": movie["id"],
        "movie_title": movie["title"],
        "showtime": showing["time"],
        "tickets": ticket_number,
        "total": total_price,
    }

    bookings.append(booking)
    showing["booked"] += ticket_number
    movies_saved = save_file(MOVIES_FILE, movies)
    bookings_saved = save_file(BOOKINGS_FILE, bookings)

    if movies_saved and bookings_saved:
        print("\nBOOKING CONFIRMED")
        print(f"Reference: {booking['id']}")
        print(f"Movie: {booking['movie_title']}")
        print(f"Tickets: {booking['tickets']}")
        print(f"Total: £{booking['total']:.2f}")
    else:
        bookings.remove(booking)
        showing["booked"] -= ticket_number
        print("The booking was not completed.")


def display_bookings(bookings):
    """Print all saved bookings."""
    if len(bookings) == 0:
        print("\nThere are no saved bookings.")
        return

    print("\nSAVED BOOKINGS")
    print("-" * 70)
    for booking in bookings:
        print(
            f"{booking['id']} | {booking['customer']} | {booking['movie_title']} | "
            f"{booking['showtime']} | {booking['tickets']} ticket(s) | "
            f"£{booking['total']:.2f}"
        )
    print("-" * 70)


def cancel_booking(movies, bookings):
    """Cancel a booking and return its seats."""
    display_bookings(bookings)
    if len(bookings) == 0:
        return

    booking_id = input("Enter the booking reference to cancel: ").strip().upper()
    selected_booking = None
    for booking in bookings:
        if booking["id"] == booking_id:
            selected_booking = booking
            break

    if selected_booking is None:
        print("Booking reference not found.")
        return

    for movie in movies:
        if movie["id"] == selected_booking["movie_id"]:
            for showing in movie["showtimes"]:
                if showing["time"] == selected_booking["showtime"]:
                    showing["booked"] -= selected_booking["tickets"]

    bookings.remove(selected_booking)
    save_file(MOVIES_FILE, movies)
    save_file(BOOKINGS_FILE, bookings)
    print("Booking cancelled.")


def show_menu():
    """Display the main menu."""
    print("\nSILVER SCREEN CINEMA")
    print("1. View all movies")
    print("2. Search for a movie")
    print("3. Sort movies")
    print("4. Book tickets")
    print("5. View bookings")
    print("6. Cancel a booking")
    print("7. Exit")


def main():
    """Load the files and run the menu until the user exits."""
    movies = load_file(MOVIES_FILE)
    bookings = load_file(BOOKINGS_FILE)
    if movies is None or bookings is None:
        print("The program cannot start without its data files.")
        return

    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            view_all_movies(movies)
        elif choice == "2":
            search_for_movie(movies)
        elif choice == "3":
            sort_movies(movies)
        elif choice == "4":
            book_tickets(movies, bookings)
        elif choice == "5":
            display_bookings(bookings)
        elif choice == "6":
            cancel_booking(movies, bookings)
        elif choice == "7":
            print("Thank you for using Silver Screen Cinema.")
            break
        else:
            print("Invalid option. Please choose 1 to 7.")


if __name__ == "__main__":
    main()
