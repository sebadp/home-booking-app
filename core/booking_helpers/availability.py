from datetime import datetime

from dateutil.parser import parse

from core.models import Booking


def check_availability(request_data:Booking) -> bool:
    """Check that Booking is available for that Property.
    TODO: REFACTOR WITH LIST OF DAYS APPROACH............. line 15. add filter with dates.
                                                            if
    """
    reservations_checked = []
    check_in = parse(request_data.get('date_start')).date()
    check_out = parse(request_data.get('date_end')).date()
    booking_list = Booking.objects.filter(rental_property=request_data.get('rental_property'))

    for booking in booking_list:
        if booking.date_start > check_out or booking.date_end < check_in:
            reservations_checked.append(True)
        else:
            reservations_checked.append(False)

    return all(reservations_checked)


def check_reservation_is_valid(request_data:Booking) -> bool:
    """Check that Booking is correct and in the future.
    Args:
        request_data: The first parameter.
    Returns:
        True for success, False otherwise.
    """
    check_in = request_data.get('date_start')
    check_out = request_data.get('date_end')
    if check_in > check_out:
        return False
    if parse(check_in).date() < datetime.now().date():
        return False
    return True
