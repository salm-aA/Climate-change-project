"""Core business logic for the cinema booking system."""

from datetime import datetime
from pathlib import Path
import uuid

from algorithms import merge_sort_movies, search_movies
from storage import load_json, save_json
from validation import validate_customer_name, validate_ticket_count


class CinemaService:
    """Manage movies, seats, bookings, searching, and sorting."""

    def __init__(self, data_folder=None):
        base_folder = Path(data_folder) if data_folder else Path(__file__).parent / "data"
        self.movies_path = base_folder / "movies.json"
        self.bookings_path = base_folder / "bookings.json"
        self.movies = load_json(str(self.movies_path), [])
        self.bookings = load_json(str(self.bookings_path), [])
        self._validate_loaded_data()

    def _validate_loaded_data(self):
        """Check essential fields so corrupt data causes a helpful error."""
        if not isinstance(self.movies, list) or not isinstance(self.bookings, list):
            raise ValueError("Cinema data must contain JSON lists.")
        required = {"id", "title", "genre", "rating", "duration", "price", "showtimes"}
        for movie in self.movies:
            if not isinstance(movie, dict) or not required.issubset(movie):
                raise ValueError("A movie record is missing required information.")

    def list_movies(self, search_text="", sort_field="title"):
        """Return movies matching a query, sorted with merge sort."""
        allowed_fields = {"title", "genre", "rating", "price"}
        if sort_field not in allowed_fields:
            sort_field = "title"
        matches = search_movies(self.movies, search_text)
        return merge_sort_movies(matches, sort_field)

    def get_movie(self, movie_id):
        """Return a movie by ID or None when it cannot be found."""
        for movie in self.movies:
            if movie["id"] == movie_id:
                return movie
        return None

    def seats_remaining(self, movie_id, showtime):
        """Return remaining seats for one movie showing."""
        movie = self.get_movie(movie_id)
        if not movie:
            raise ValueError("The selected movie no longer exists.")
        showing = self._find_showing(movie, showtime)
        return showing["capacity"] - showing["booked"]

    @staticmethod
    def _find_showing(movie, showtime):
        """Return the selected showing or raise a helpful error."""
        for showing in movie["showtimes"]:
            if showing["time"] == showtime:
                return showing
        raise ValueError("The selected showtime is not available.")

    def create_booking(self, customer_name, movie_id, showtime, ticket_value):
        """Validate, create, persist, and return a new booking."""
        customer = validate_customer_name(customer_name)
        tickets = validate_ticket_count(ticket_value)
        movie = self.get_movie(movie_id)
        if not movie:
            raise ValueError("Please select an available movie.")
        showing = self._find_showing(movie, showtime)
        remaining = showing["capacity"] - showing["booked"]
        if tickets > remaining:
            raise ValueError(f"Only {remaining} seat(s) remain for this showtime.")

        booking = {
            "id": uuid.uuid4().hex[:8].upper(),
            "customer": customer,
            "movie_id": movie_id,
            "movie_title": movie["title"],
            "showtime": showtime,
            "tickets": tickets,
            "total": round(movie["price"] * tickets, 2),
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        }

        showing["booked"] += tickets
        self.bookings.append(booking)
        try:
            self._save_all()
        except Exception:
            showing["booked"] -= tickets
            self.bookings.pop()
            raise
        return booking

    def cancel_booking(self, booking_id):
        """Cancel a booking, restore its seats, and save the change."""
        for index, booking in enumerate(self.bookings):
            if booking["id"] == booking_id:
                movie = self.get_movie(booking["movie_id"])
                if not movie:
                    raise ValueError("The movie linked to this booking is missing.")
                showing = self._find_showing(movie, booking["showtime"])
                removed = self.bookings.pop(index)
                showing["booked"] = max(0, showing["booked"] - booking["tickets"])
                try:
                    self._save_all()
                except Exception:
                    self.bookings.insert(index, removed)
                    showing["booked"] += booking["tickets"]
                    raise
                return removed
        raise ValueError("The selected booking could not be found.")

    def _save_all(self):
        """Save movies and bookings to their JSON files."""
        save_json(str(self.movies_path), self.movies)
        save_json(str(self.bookings_path), self.bookings)
