import pytest

from easy_booking.exceptions.base import Conflict, NotFound
from easy_booking.exceptions.room import RoomLinkedToAnotherObject, RoomNotFound


class TestRoomExceptions:
    def test_room_not_found_exception(self):
        exception = RoomNotFound()

        assert isinstance(exception, NotFound)

        assert exception.detail == "Room with the given id doesn't exist"

        with pytest.raises(RoomNotFound) as excinfo:
            raise RoomNotFound()

        assert str(excinfo.value) == "404: Room with the given id doesn't exist"

    def test_room_linked_to_another_object_exception(self):
        exception = RoomLinkedToAnotherObject()

        assert isinstance(exception, Conflict)

        assert exception.detail == "Room is linked to another object and can't be deleted"

        with pytest.raises(RoomLinkedToAnotherObject) as excinfo:
            raise RoomLinkedToAnotherObject()

        assert str(excinfo.value) == "409: Room is linked to another object and can't be deleted"

    def test_exception_hierarchy(self):
        assert issubclass(RoomNotFound, NotFound)

        assert issubclass(RoomLinkedToAnotherObject, Conflict)

        assert not issubclass(NotFound, Conflict)
        assert not issubclass(Conflict, NotFound)


class TestExceptionMessaging:
    def test_room_not_found_repr(self):
        exception = RoomNotFound()
        repr_str = repr(exception)
        assert "RoomNotFound" in repr_str
        assert "Room with the given id doesn't exist" in repr_str

    def test_room_linked_repr(self):
        exception = RoomLinkedToAnotherObject()
        repr_str = repr(exception)
        assert "RoomLinkedToAnotherObject" in repr_str
        assert "Room is linked to another object and can't be deleted" in repr_str

