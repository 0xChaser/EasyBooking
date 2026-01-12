import pytest

from easy_booking.exceptions.base import Conflict, NotFound
from easy_booking.exceptions.user import UserLinkedToAnotherObject, UserNotFound


class TestUserExceptions:
    def test_user_not_found_exception(self):
        exception = UserNotFound()

        assert isinstance(exception, NotFound)

        assert exception.detail == "User with the given id doesn't exist"

        with pytest.raises(UserNotFound) as excinfo:
            raise UserNotFound()

        assert str(excinfo.value) == "404: User with the given id doesn't exist"

    def test_user_linked_to_another_object_exception(self):
        exception = UserLinkedToAnotherObject()

        assert isinstance(exception, Conflict)

        assert exception.detail == "User is linked to another object and can't be deleted"

        with pytest.raises(UserLinkedToAnotherObject) as excinfo:
            raise UserLinkedToAnotherObject()

        assert str(excinfo.value) == "409: User is linked to another object and can't be deleted"

    def test_exception_hierarchy(self):
        assert issubclass(UserNotFound, NotFound)

        assert issubclass(UserLinkedToAnotherObject, Conflict)

        assert not issubclass(NotFound, Conflict)
        assert not issubclass(Conflict, NotFound)


class TestExceptionMessaging:
    def test_user_not_found_repr(self):
        exception = UserNotFound()
        repr_str = repr(exception)
        assert "UserNotFound" in repr_str
        assert "User with the given id doesn't exist" in repr_str

    def test_user_linked_repr(self):
        exception = UserLinkedToAnotherObject()
        repr_str = repr(exception)
        assert "UserLinkedToAnotherObject" in repr_str
        assert "User is linked to another object and can't be deleted" in repr_str