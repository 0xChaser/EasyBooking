import pytest

from easy_booking.exceptions.base import Conflict, NotFound
from easy_booking.exceptions.booking import BookingLinkedToAnotherObject, BookingNotFound


class TestBookingExceptions:
    def test_booking_not_found_exception(self):
        exception = BookingNotFound()

        assert isinstance(exception, NotFound)

        assert exception.detail == "Booking with the given id doesn't exist"

        with pytest.raises(BookingNotFound) as excinfo:
            raise BookingNotFound()

        assert str(excinfo.value) == "404: Booking with the given id doesn't exist"

    def test_booking_linked_to_another_object_exception(self):
        exception = BookingLinkedToAnotherObject()

        assert isinstance(exception, Conflict)

        assert exception.detail == "Booking is linked to another object and can't be deleted"

        with pytest.raises(BookingLinkedToAnotherObject) as excinfo:
            raise BookingLinkedToAnotherObject()

        assert str(excinfo.value) == "409: Booking is linked to another object and can't be deleted"

    def test_exception_hierarchy(self):
        assert issubclass(BookingNotFound, NotFound)

        assert issubclass(BookingLinkedToAnotherObject, Conflict)

        assert not issubclass(NotFound, Conflict)
        assert not issubclass(Conflict, NotFound)


class TestExceptionMessaging:
    def test_booking_not_found_repr(self):
        exception = BookingNotFound()
        repr_str = repr(exception)
        assert "BookingNotFound" in repr_str
        assert "Booking with the given id doesn't exist" in repr_str

    def test_booking_linked_repr(self):
        exception = BookingLinkedToAnotherObject()
        repr_str = repr(exception)
        assert "BookingLinkedToAnotherObject" in repr_str
        assert "Booking is linked to another object and can't be deleted" in repr_str

