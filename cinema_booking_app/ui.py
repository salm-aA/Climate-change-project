"""Tkinter user interface for the cinema booking system."""

import tkinter as tk
from tkinter import messagebox, ttk

from storage import StorageError


class CinemaApp:
    """Display movies and allow customers to make and cancel bookings."""

    SORT_FIELDS = {
        "Title": "title",
        "Genre": "genre",
        "Rating": "rating",
        "Price": "price",
    }

    def __init__(self, root, service):
        self.root = root
        self.service = service
        self.movie_ids = []
        self.selected_movie_id = None

        root.title("Silver Screen Cinema Booking")
        root.geometry("960x650")
        root.minsize(820, 560)
        self._configure_style()
        self._build_interface()
        self.refresh_movies()
        self.refresh_bookings()

    def _configure_style(self):
        """Configure a clear, consistent visual style."""
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Title.TLabel", font=("Arial", 22, "bold"), foreground="#19324d")
        style.configure("Heading.TLabel", font=("Arial", 12, "bold"))
        style.configure("Treeview", rowheight=28, font=("Arial", 10))
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        style.configure("Accent.TButton", font=("Arial", 10, "bold"))

    def _build_interface(self):
        """Create all interface controls and layouts."""
        outer = ttk.Frame(self.root, padding=18)
        outer.pack(fill="both", expand=True)
        ttk.Label(outer, text="Silver Screen Cinema", style="Title.TLabel").pack(anchor="w")
        ttk.Label(outer, text="Find a film, choose a showing, and reserve your seats.").pack(
            anchor="w", pady=(2, 14)
        )

        notebook = ttk.Notebook(outer)
        notebook.pack(fill="both", expand=True)
        movies_tab = ttk.Frame(notebook, padding=12)
        bookings_tab = ttk.Frame(notebook, padding=12)
        notebook.add(movies_tab, text="Movies and booking")
        notebook.add(bookings_tab, text="Manage bookings")
        self._build_movies_tab(movies_tab)
        self._build_bookings_tab(bookings_tab)

    def _build_movies_tab(self, parent):
        """Build the movie browsing and booking tab."""
        tools = ttk.Frame(parent)
        tools.pack(fill="x", pady=(0, 10))
        ttk.Label(tools, text="Search title or genre:").pack(side="left")
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(tools, textvariable=self.search_var, width=28)
        search_entry.pack(side="left", padx=(6, 14))
        search_entry.bind("<Return>", lambda _event: self.refresh_movies())
        ttk.Button(tools, text="Search", command=self.refresh_movies).pack(side="left")
        ttk.Button(tools, text="Clear", command=self.clear_search).pack(side="left", padx=5)
        ttk.Label(tools, text="Sort by:").pack(side="left", padx=(20, 5))
        self.sort_var = tk.StringVar(value="Title")
        sort_box = ttk.Combobox(
            tools, textvariable=self.sort_var, values=list(self.SORT_FIELDS), state="readonly", width=10
        )
        sort_box.pack(side="left")
        sort_box.bind("<<ComboboxSelected>>", lambda _event: self.refresh_movies())

        columns = ("title", "genre", "rating", "duration", "price")
        self.movie_tree = ttk.Treeview(parent, columns=columns, show="headings", height=11)
        headings = ("Movie", "Genre", "Rating", "Minutes", "Ticket price")
        widths = (270, 150, 80, 90, 100)
        for column, heading, width in zip(columns, headings, widths):
            self.movie_tree.heading(column, text=heading)
            self.movie_tree.column(column, width=width, anchor="center" if column != "title" else "w")
        self.movie_tree.pack(fill="both", expand=True)
        self.movie_tree.bind("<<TreeviewSelect>>", self.on_movie_selected)

        booking = ttk.LabelFrame(parent, text="Book selected movie", padding=12)
        booking.pack(fill="x", pady=(12, 0))
        self.selection_label = ttk.Label(booking, text="Select a movie above.", style="Heading.TLabel")
        self.selection_label.grid(row=0, column=0, columnspan=6, sticky="w", pady=(0, 9))
        ttk.Label(booking, text="Customer name:").grid(row=1, column=0, sticky="w")
        self.name_var = tk.StringVar()
        ttk.Entry(booking, textvariable=self.name_var, width=24).grid(row=1, column=1, padx=(6, 18))
        ttk.Label(booking, text="Showtime:").grid(row=1, column=2, sticky="w")
        self.showtime_var = tk.StringVar()
        self.showtime_box = ttk.Combobox(booking, textvariable=self.showtime_var, state="readonly", width=17)
        self.showtime_box.grid(row=1, column=3, padx=(6, 18))
        self.showtime_box.bind("<<ComboboxSelected>>", lambda _event: self.update_seat_label())
        ttk.Label(booking, text="Tickets:").grid(row=1, column=4, sticky="w")
        self.ticket_var = tk.StringVar(value="1")
        ttk.Spinbox(booking, from_=1, to=10, textvariable=self.ticket_var, width=5).grid(
            row=1, column=5, padx=(6, 12)
        )
        self.seat_label = ttk.Label(booking, text="")
        self.seat_label.grid(row=2, column=0, columnspan=4, sticky="w", pady=(10, 0))
        ttk.Button(booking, text="Confirm booking", style="Accent.TButton", command=self.book).grid(
            row=2, column=4, columnspan=2, sticky="e", pady=(10, 0)
        )

    def _build_bookings_tab(self, parent):
        """Build the booking management tab."""
        ttk.Label(parent, text="Current bookings", style="Heading.TLabel").pack(anchor="w", pady=(0, 8))
        columns = ("id", "customer", "movie", "showtime", "tickets", "total")
        self.booking_tree = ttk.Treeview(parent, columns=columns, show="headings", height=14)
        headings = ("Reference", "Customer", "Movie", "Showtime", "Tickets", "Total")
        widths = (90, 150, 240, 145, 70, 80)
        for column, heading, width in zip(columns, headings, widths):
            self.booking_tree.heading(column, text=heading)
            self.booking_tree.column(column, width=width, anchor="center" if column != "movie" else "w")
        self.booking_tree.pack(fill="both", expand=True)
        controls = ttk.Frame(parent)
        controls.pack(fill="x", pady=(12, 0))
        ttk.Button(controls, text="Refresh", command=self.refresh_bookings).pack(side="left")
        ttk.Button(controls, text="Cancel selected booking", command=self.cancel_booking).pack(side="right")

    def clear_search(self):
        """Clear the search box and show all movies."""
        self.search_var.set("")
        self.refresh_movies()

    def refresh_movies(self):
        """Reload filtered and sorted movie rows."""
        for row in self.movie_tree.get_children():
            self.movie_tree.delete(row)
        sort_field = self.SORT_FIELDS.get(self.sort_var.get(), "title")
        movies = self.service.list_movies(self.search_var.get(), sort_field)
        self.movie_ids = []
        for movie in movies:
            self.movie_ids.append(movie["id"])
            self.movie_tree.insert(
                "", "end", values=(movie["title"], movie["genre"], movie["rating"], movie["duration"], f"£{movie['price']:.2f}")
            )
        if not movies:
            self.selection_label.config(text="No movies match this search.")

    def on_movie_selected(self, _event=None):
        """Update booking choices after a movie row is selected."""
        selection = self.movie_tree.selection()
        if not selection:
            return
        index = self.movie_tree.index(selection[0])
        if index >= len(self.movie_ids):
            return
        self.selected_movie_id = self.movie_ids[index]
        movie = self.service.get_movie(self.selected_movie_id)
        self.selection_label.config(text=f"{movie['title']} — {movie['genre']} — £{movie['price']:.2f} per ticket")
        times = [showing["time"] for showing in movie["showtimes"]]
        self.showtime_box["values"] = times
        self.showtime_var.set(times[0] if times else "")
        self.update_seat_label()

    def update_seat_label(self):
        """Show remaining seats for the current movie and showtime."""
        if not self.selected_movie_id or not self.showtime_var.get():
            self.seat_label.config(text="")
            return
        try:
            seats = self.service.seats_remaining(self.selected_movie_id, self.showtime_var.get())
            self.seat_label.config(text=f"Seats remaining for this showing: {seats}")
        except ValueError as error:
            self.seat_label.config(text=str(error))

    def book(self):
        """Create a booking from the form and display its reference."""
        try:
            booking = self.service.create_booking(
                self.name_var.get(), self.selected_movie_id, self.showtime_var.get(), self.ticket_var.get()
            )
        except (ValueError, StorageError) as error:
            messagebox.showerror("Booking not completed", str(error))
            return
        messagebox.showinfo(
            "Booking confirmed",
            f"Reference: {booking['id']}\nMovie: {booking['movie_title']}\nTotal: £{booking['total']:.2f}",
        )
        self.name_var.set("")
        self.ticket_var.set("1")
        self.update_seat_label()
        self.refresh_bookings()

    def refresh_bookings(self):
        """Reload all booking rows."""
        for row in self.booking_tree.get_children():
            self.booking_tree.delete(row)
        for booking in self.service.bookings:
            self.booking_tree.insert(
                "", "end", values=(booking["id"], booking["customer"], booking["movie_title"], booking["showtime"], booking["tickets"], f"£{booking['total']:.2f}")
            )

    def cancel_booking(self):
        """Ask for confirmation and cancel the selected booking."""
        selection = self.booking_tree.selection()
        if not selection:
            messagebox.showwarning("No booking selected", "Select a booking to cancel.")
            return
        booking_id = self.booking_tree.item(selection[0], "values")[0]
        if not messagebox.askyesno("Cancel booking", f"Cancel booking {booking_id} and restore its seats?"):
            return
        try:
            self.service.cancel_booking(booking_id)
        except (ValueError, StorageError) as error:
            messagebox.showerror("Cancellation failed", str(error))
            return
        self.refresh_bookings()
        self.update_seat_label()
        messagebox.showinfo("Booking cancelled", "The booking was cancelled and its seats were restored.")
