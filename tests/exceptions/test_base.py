import pytest
from fastapi import HTTPException

from easy_booking.exceptions.base import Unauthorized, NotFound, Conflict


def test_unauthorized_exception():
    exc = Unauthorized(detail="Not authenticated")
    assert isinstance(exc, HTTPException)
    assert exc.status_code == 401
    assert exc.detail == "Not authenticated"


def test_not_found_exception():
    exc = NotFound(detail="Item not found")
    assert isinstance(exc, HTTPException)
    assert exc.status_code == 404
    assert exc.detail == "Item not found"


def test_conflict_exception():
    exc = Conflict(detail="Conflict occurred")
    assert isinstance(exc, HTTPException)
    assert exc.status_code == 409
    assert exc.detail == "Conflict occurred"