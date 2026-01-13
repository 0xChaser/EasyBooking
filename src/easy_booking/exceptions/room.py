from easy_booking.exceptions.base import Conflict, NotFound, BadRequest

class RoomNotFound(NotFound):
    def __init__(self) -> None:
        detail = "Room with the given id doesn't exist" 
        super().__init__(detail)

class RoomLinkedToAnotherObject(Conflict):
    def __init__(self) -> None:
        detail = "Room is linked to another object and can't be deleted"
        super().__init__(detail)

class RoomUnavailable(BadRequest):
    def __init__(self, status: str = "unavailable") -> None:
        detail = f"Room is currently {status} and cannot be booked"
        super().__init__(detail)