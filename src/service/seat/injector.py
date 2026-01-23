"""
Seat Context Injector

Attaches immutable SeatContext to the execution envelope
at ingress.
"""

from typing import Dict, Any
from src.service.seat.context import SeatContext


def inject_seat_context(
    envelope: Dict[str, Any],
    seat_record: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Attach SeatContext to the envelope.

    Assumes:
    - seat_record is trusted and validated
    - envelope is mutable at ingress only
    """

    envelope["seat_context"] = SeatContext(
        seat_id=seat_record["seat_id"],
        seat_name=seat_record["seat_name"],
    )

    return envelope
