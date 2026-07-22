"""Cinema ticket booking application made with Python and Tkinter."""

import json
import os
import tkinter as tk
from tkinter import messagebox, ttk

from algorithms import merge_sort, search_movies


# File locations are based on the folder containing this program.
PROGRAM_FOLDER = os.path.dirname(os.path.abspath(__file__))
MOVIES_FILE = os.path.join(PROGRAM_FOLDER, "data", "movies.json")
BOOKINGS_FILE = os.path.join(PROGRAM_FOLDER, "data", "bookings.json")

# These lists are filled when the program starts.
movies = []
bookings = []
displayed_movies = []


def load_json(filename):
    """Read and return a list from a JSON file."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
        if not isinstance(data, list):
            raise ValueError("The file must contain a list.")
        return data
    except FileNotFoundError as error:
        raise ValueError(f"File not found: {filename}") from error
    except json.JSONDecodeError as error:
        raise ValueError(f"The file contains invalid JSON: {filename}") from error
    except OSError as error:
        raise ValueError(f"The file could not be opened: {filename}") from error


def save_json(filename, data):
    """Write a list to a JSON file."""
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)
    except OSError as error:
        raise ValueError(f"The file could not be saved: {filename}") from error


def find_movie(movie_id):
    """Find one movie by its ID."""
    for movie in movies:
        if movie["id"] == movie_id:
            return movie
    return None


def find_showtime(movie, selected_time):
    """Find one showtime inside a movie dictionary."""
    for showing in movie["showtimes"]:
        if showing["time"] == selected_time:
            return showing
    return None


def check_name(name):
    """Check and clean the customer's name."""
    name = name.strip()
    if len(name) < 2:
        raise ValueError("Please enter at least two characters for the name.")
    if len(name) > 60:
        raise ValueError("The name must be 60 characters or fewer.")
    return name


def check_ticket_number(ticket_text):
    """Convert the ticket entry to a valid whole number."""
    try:
        ticket_number = int(ticket_text)
    except (TypeError, ValueError) as error:
        raise ValueError("Tickets must be entered as a whole number.") from error

    if ticket_number < 1 or ticket_number > 10:
        raise ValueError("You can book between 1 and 10 tickets.")
    return ticket_number


def next_booking_id():
    """Create the next simple booking reference, for example B001."""
    highest_number = 0
    for booking in bookings:
        try:
            number = int(booking["id"].replace("B", ""))
            if number > highest_number:
                highest_number = number
        except (KeyError, ValueError):
            continue
    return f"B{highest_number + 1:03d}"


def make_booking(customer, movie_id, selected_time, ticket_text):
    """Validate and create a booking, then save it to the files."""
    customer = check_name(customer)
    ticket_number = check_ticket_number(ticket_text)
    movie = find_movie(movie_id)
    if movie is None:
        raise ValueError("Please select a movie.")

    showing = find_showtime(movie, selected_time)
    if showing is None:
        raise ValueError("Please select a valid showtime.")

    seats_left = showing["capacity"] - showing["booked"]
    if ticket_number > seats_left:
        raise ValueError(f"Only {seats_left} seat(s) are available.")

    # Arithmetic is used to calculate the total ticket price.
    total_price = round(movie["price"] * ticket_number, 2)
    booking = {
        "id": next_booking_id(),
        "customer": customer,
        "movie_id": movie["id"],
        "movie_title": movie["title"],
        "showtime": selected_time,
        "tickets": ticket_number,
        "total": total_price,
    }

    showing["booked"] += ticket_number
    bookings.append(booking)
    try:
        save_json(MOVIES_FILE, movies)
        save_json(BOOKINGS_FILE, bookings)
    except ValueError:
        # Undo the change in memory if saving fails.
        showing["booked"] -= ticket_number
        bookings.remove(booking)
        raise
    return booking


def cancel_booking(booking_id):
    """Remove a booking and return its seats to the showtime."""
    for booking in bookings:
        if booking["id"] == booking_id:
            movie = find_movie(booking["movie_id"])
            if movie is None:
                raise ValueError("The movie connected to this booking is missing.")
            showing = find_showtime(movie, booking["showtime"])
            if showing is None:
                raise ValueError("The showtime connected to this booking is missing.")

            bookings.remove(booking)
            showing["booked"] -= booking["tickets"]
            try:
                save_json(MOVIES_FILE, movies)
                save_json(BOOKINGS_FILE, bookings)
            except ValueError:
                bookings.append(booking)
                showing["booked"] += booking["tickets"]
                raise
            return booking
    raise ValueError("The selected booking could not be found.")


def refresh_movie_table():
    """Search, sort, and display movies in the table."""
    global displayed_movies
    for row in movie_table.get_children():
        movie_table.delete(row)

    matching_movies = search_movies(movies, search_text.get())
    sort_field = sort_choices[sort_text.get()]
    displayed_movies = merge_sort(matching_movies, sort_field)

    for movie in displayed_movies:
        movie_table.insert(
            "",
            "end",
            values=(
                movie["title"],
                movie["genre"],
                movie["rating"],
                movie["duration"],
                f"£{movie['price']:.2f}",
            ),
        )


def clear_search():
    """Clear the search entry and display every movie."""
    search_text.set("")
    refresh_movie_table()


def selected_movie():
    """Return the movie selected in the table, or None."""
    selected_rows = movie_table.selection()
    if not selected_rows:
        return None
    row_number = movie_table.index(selected_rows[0])
    if row_number >= len(displayed_movies):
        return None
    return displayed_movies[row_number]


def movie_was_selected(event=None):
    """Display the available showtimes for the selected movie."""
    movie = selected_movie()
    if movie is None:
        return
    movie_details.config(
        text=f"{movie['title']} - {movie['genre']} - £{movie['price']:.2f} per ticket"
    )
    available_times = []
    for showing in movie["showtimes"]:
        available_times.append(showing["time"])
    showtime_box["values"] = available_times
    showtime_text.set(available_times[0] if available_times else "")
    update_seat_message()


def update_seat_message(event=None):
    """Show the number of seats remaining for the selected showing."""
    movie = selected_movie()
    if movie is None:
        seat_message.config(text="")
        return
    showing = find_showtime(movie, showtime_text.get())
    if showing is None:
        seat_message.config(text="")
        return
    seats_left = showing["capacity"] - showing["booked"]
    seat_message.config(text=f"Seats remaining: {seats_left}")


def book_from_form():
    """Create a booking using the entries on the screen."""
    movie = selected_movie()
    movie_id = movie["id"] if movie else None
    try:
        booking = make_booking(
            customer_text.get(), movie_id, showtime_text.get(), ticket_text.get()
        )
    except ValueError as error:
        messagebox.showerror("Booking not completed", str(error))
        return

    messagebox.showinfo(
        "Booking confirmed",
        f"Reference: {booking['id']}\n"
        f"Movie: {booking['movie_title']}\n"
        f"Total: £{booking['total']:.2f}",
    )
    customer_text.set("")
    ticket_text.set("1")
    update_seat_message()
    refresh_booking_table()


def refresh_booking_table():
    """Display all saved bookings in the booking table."""
    for row in booking_table.get_children():
        booking_table.delete(row)
    for booking in bookings:
        booking_table.insert(
            "",
            "end",
            values=(
                booking["id"],
                booking["customer"],
                booking["movie_title"],
                booking["showtime"],
                booking["tickets"],
                f"£{booking['total']:.2f}",
            ),
        )


def cancel_selected_booking():
    """Cancel the booking selected in the booking table."""
    selected_rows = booking_table.selection()
    if not selected_rows:
        messagebox.showwarning("No booking selected", "Please select a booking.")
        return
    booking_id = booking_table.item(selected_rows[0], "values")[0]
    answer = messagebox.askyesno("Cancel booking", f"Cancel booking {booking_id}?")
    if not answer:
        return
    try:
        cancel_booking(booking_id)
    except ValueError as error:
        messagebox.showerror("Cancellation failed", str(error))
        return
    refresh_booking_table()
    update_seat_message()
    messagebox.showinfo("Booking cancelled", "The seats have been returned.")


def create_interface():
    """Create and run the Tkinter user interface."""
    global root, movie_table, booking_table, movie_details, showtime_box, seat_message
    global search_text, sort_text, customer_text, showtime_text, ticket_text

    root = tk.Tk()
    root.title("Silver Screen Cinema")
    root.geometry("950x640")
    root.minsize(800, 550)

    search_text = tk.StringVar()
    sort_text = tk.StringVar(value="Title")
    customer_text = tk.StringVar()
    showtime_text = tk.StringVar()
    ticket_text = tk.StringVar(value="1")

    page = ttk.Frame(root, padding=16)
    page.pack(fill="both", expand=True)
    ttk.Label(page, text="Silver Screen Cinema", font=("Arial", 22, "bold")).pack(anchor="w")
    ttk.Label(page, text="Browse films and book cinema tickets.").pack(anchor="w", pady=(2, 12))

    tabs = ttk.Notebook(page)
    tabs.pack(fill="both", expand=True)
    movie_tab = ttk.Frame(tabs, padding=10)
    booking_tab = ttk.Frame(tabs, padding=10)
    tabs.add(movie_tab, text="Movies")
    tabs.add(booking_tab, text="Bookings")

    search_frame = ttk.Frame(movie_tab)
    search_frame.pack(fill="x", pady=(0, 8))
    ttk.Label(search_frame, text="Search:").pack(side="left")
    search_entry = ttk.Entry(search_frame, textvariable=search_text, width=25)
    search_entry.pack(side="left", padx=5)
    search_entry.bind("<Return>", lambda event: refresh_movie_table())
    ttk.Button(search_frame, text="Search", command=refresh_movie_table).pack(side="left")
    ttk.Button(search_frame, text="Clear", command=clear_search).pack(side="left", padx=5)
    ttk.Label(search_frame, text="Sort by:").pack(side="left", padx=(20, 5))
    sort_box = ttk.Combobox(
        search_frame, textvariable=sort_text, values=list(sort_choices), state="readonly", width=10
    )
    sort_box.pack(side="left")
    sort_box.bind("<<ComboboxSelected>>", lambda event: refresh_movie_table())

    movie_columns = ("title", "genre", "rating", "duration", "price")
    movie_table = ttk.Treeview(movie_tab, columns=movie_columns, show="headings", height=10)
    movie_headings = ("Movie", "Genre", "Rating", "Minutes", "Price")
    movie_widths = (260, 150, 80, 90, 90)
    for column, heading, width in zip(movie_columns, movie_headings, movie_widths):
        movie_table.heading(column, text=heading)
        movie_table.column(column, width=width, anchor="center")
    movie_table.pack(fill="both", expand=True)
    movie_table.bind("<<TreeviewSelect>>", movie_was_selected)

    form = ttk.LabelFrame(movie_tab, text="Book selected movie", padding=10)
    form.pack(fill="x", pady=(10, 0))
    movie_details = ttk.Label(form, text="Select a movie above.", font=("Arial", 11, "bold"))
    movie_details.grid(row=0, column=0, columnspan=6, sticky="w", pady=(0, 8))
    ttk.Label(form, text="Name:").grid(row=1, column=0)
    ttk.Entry(form, textvariable=customer_text, width=22).grid(row=1, column=1, padx=(5, 15))
    ttk.Label(form, text="Showtime:").grid(row=1, column=2)
    showtime_box = ttk.Combobox(form, textvariable=showtime_text, state="readonly", width=17)
    showtime_box.grid(row=1, column=3, padx=(5, 15))
    showtime_box.bind("<<ComboboxSelected>>", update_seat_message)
    ttk.Label(form, text="Tickets:").grid(row=1, column=4)
    ttk.Spinbox(form, from_=1, to=10, textvariable=ticket_text, width=5).grid(row=1, column=5, padx=5)
    seat_message = ttk.Label(form)
    seat_message.grid(row=2, column=0, columnspan=4, sticky="w", pady=(8, 0))
    ttk.Button(form, text="Confirm booking", command=book_from_form).grid(
        row=2, column=4, columnspan=2, sticky="e", pady=(8, 0)
    )

    ttk.Label(booking_tab, text="Saved bookings", font=("Arial", 12, "bold")).pack(anchor="w")
    booking_columns = ("id", "customer", "movie", "showtime", "tickets", "total")
    booking_table = ttk.Treeview(booking_tab, columns=booking_columns, show="headings", height=14)
    booking_headings = ("Reference", "Customer", "Movie", "Showtime", "Tickets", "Total")
    booking_widths = (85, 140, 230, 145, 65, 80)
    for column, heading, width in zip(booking_columns, booking_headings, booking_widths):
        booking_table.heading(column, text=heading)
        booking_table.column(column, width=width, anchor="center")
    booking_table.pack(fill="both", expand=True, pady=(8, 10))
    ttk.Button(booking_tab, text="Cancel selected booking", command=cancel_selected_booking).pack(
        anchor="e"
    )

    refresh_movie_table()
    refresh_booking_table()
    root.mainloop()


def start_program():
    """Load the files and start the application."""
    global movies, bookings, sort_choices
    try:
        movies = load_json(MOVIES_FILE)
        bookings = load_json(BOOKINGS_FILE)
    except ValueError as error:
        error_window = tk.Tk()
        error_window.withdraw()
        messagebox.showerror("Data error", str(error))
        error_window.destroy()
        return

    sort_choices = {
        "Title": "title",
        "Genre": "genre",
        "Rating": "rating",
        "Price": "price",
    }
    create_interface()


if __name__ == "__main__":
    start_program()
