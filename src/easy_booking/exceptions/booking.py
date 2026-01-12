from easy_booking.exceptions.base import Conflict, NotFound

class BookingNotFound(NotFound):
    def __init__(self) -> None:
        detail = "Booking with the given id doesn't exist" 
        super().__init__(detail)

class BookingLinkedToAnotherObject(Conflict):
    def __init__(self) -> None:
        detail = "Booking is linked to another object and can't be deleted"
        super().__init__(detail)