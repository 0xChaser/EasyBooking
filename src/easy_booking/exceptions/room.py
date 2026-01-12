from easy_booking.exceptions.base import Conflict, NotFound

class RoomNotFound(NotFound):
    def __init__(self) -> None:
        detail = "Room with the given id doesn't exist" 
        super().__init__(detail)

class RoomLinkedToAnotherObject(Conflict):
    def __init__(self) -> None:
        detail = "Room is linked to another object and can't be deleted"
        super().__init__(detail)