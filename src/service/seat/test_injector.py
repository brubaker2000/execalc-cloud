from src.service.seat.injector import inject_seat_context
from src.service.seat.context import SeatContext


def test_inject_seat_context_attaches_context():
    envelope = {}
    seat_record = {
        "seat_id": "seat_001",
        "seat_name": "Board Member A",
    }

    result = inject_seat_context(envelope, seat_record)

    assert "seat_context" in result
    assert isinstance(result["seat_context"], SeatContext)
    assert result["seat_context"].seat_id == "seat_001"
    assert result["seat_context"].seat_name == "Board Member A"
