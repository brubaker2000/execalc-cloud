"""
Seat Context

Immutable identity for an acting seat (user, agent, or actor)
within a tenant namespace.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class SeatContext:
    """
    Immutable seat identity.
    """

    seat_id: str
    seat_name: str
