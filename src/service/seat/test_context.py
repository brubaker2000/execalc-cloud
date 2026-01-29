import unittest

from src.service.seat.context import SeatContext


class TestSeatContext(unittest.TestCase):
    def test_seat_context_is_immutable(self):
        seat = SeatContext(seat_id="seat_001", seat_name="Board Member A")

        self.assertEqual(seat.seat_id, "seat_001")
        self.assertEqual(seat.seat_name, "Board Member A")

        with self.assertRaises(Exception):
            seat.seat_name = "Mutated"


if __name__ == "__main__":
    unittest.main()
