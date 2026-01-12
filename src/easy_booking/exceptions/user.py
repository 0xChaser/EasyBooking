
from easy_booking.exceptions.base import Conflict, NotFound

class UserNotFound(NotFound):
    def __init__(self) -> None:
        detail = "User with the given id doesn't exist"
        super().__init__(detail)

class UserLinkedToAnotherObject(Conflict):
    def __init__(self) -> None:
        detail = "User is linked to another object and can't be deleted"
        super().__init__(detail)