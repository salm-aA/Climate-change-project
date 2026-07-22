"""Automated tests for cinema algorithms and booking logic."""

import json
from pathlib import Path
import tempfile
import unittest

from algorithms import merge_sort_movies, recursive_binary_search, search_movies
from cinema import CinemaService


SAMPLE_MOVIES = [
    {
        "id": "M2", "title": "Zulu", "genre": "Drama", "rating": 7.0,
        "duration": 100, "price": 5.0,
        "showtimes": [{"time": "Tomorrow 18:00", "capacity": 5, "booked": 1}],
    },
    {
        "id": "M1", "title": "Alpha", "genre": "Comedy", "rating": 8.0,
        "duration": 90, "price": 6.0,
        "showtimes": [{"time": "Tomorrow 16:00", "capacity": 5, "booked": 0}],
    },
]


class AlgorithmTests(unittest.TestCase):
    def test_merge_sort_orders_titles(self):
        result = merge_sort_movies(SAMPLE_MOVIES, "title")
        self.assertEqual([movie["title"] for movie in result], ["Alpha", "Zulu"])

    def test_recursive_binary_search_finds_exact_title(self):
        ordered = merge_sort_movies(SAMPLE_MOVIES, "title")
        self.assertEqual(recursive_binary_search(ordered, "zulu")["id"], "M2")

    def test_partial_search_finds_genre(self):
        self.assertEqual(search_movies(SAMPLE_MOVIES, "come")[0]["id"], "M1")


class BookingTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        path = Path(self.folder.name)
        (path / "movies.json").write_text(json.dumps(SAMPLE_MOVIES), encoding="utf-8")
        (path / "bookings.json").write_text("[]", encoding="utf-8")
        self.service = CinemaService(path)

    def tearDown(self):
        self.folder.cleanup()

    def test_booking_reduces_seats_and_calculates_total(self):
        booking = self.service.create_booking("Alex Smith", "M1", "Tomorrow 16:00", 2)
        self.assertEqual(booking["total"], 12.0)
        self.assertEqual(self.service.seats_remaining("M1", "Tomorrow 16:00"), 3)

    def test_too_many_tickets_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "Only 4 seat"):
            self.service.create_booking("Alex Smith", "M2", "Tomorrow 18:00", 5)

    def test_cancellation_restores_seats(self):
        booking = self.service.create_booking("Alex Smith", "M1", "Tomorrow 16:00", 2)
        self.service.cancel_booking(booking["id"])
        self.assertEqual(self.service.seats_remaining("M1", "Tomorrow 16:00"), 5)

    def test_invalid_customer_and_ticket_inputs_are_rejected(self):
        with self.assertRaises(ValueError):
            self.service.create_booking("", "M1", "Tomorrow 16:00", 1)
        with self.assertRaises(ValueError):
            self.service.create_booking("Alex Smith", "M1", "Tomorrow 16:00", "two")


if __name__ == "__main__":
    unittest.main()
