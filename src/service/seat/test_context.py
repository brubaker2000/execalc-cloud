from src.service.seat.context import SeatContext
import pytest


def test_seat_context_is_immutable():
    seat = SeatContext(
        seat_id="seat_001",
        seat_name="Board Member A",
    )

    assert seat.seat_id == "seat_001"
    assert seat.seat_name == "Board Member A"

    with pytest.raises(Exception):
        seat.seat_name = "Mutated"
