import json
import requests


def get_availability_by_stylist_by_date(stylist, date):
    result = requests.get(
        'http://127.0.0.1:5001/availability/{}/{}'.format(stylist, date),
        headers={'content-type': 'application/json'}
    )
    return result.json()


def add_new_booking(customer_id, stylist_id, treatment_id, booking_date, booking_time):

    booking = {
        "customer_id": customer_id,
        "stylist_id": stylist_id,
        "treatment_id": treatment_id,
        "booking_date": booking_date,
        "booking_time": booking_time
    }

    result = requests.post(
        'http://127.0.0.1:5001/booking',
        headers={'content-type': 'application/json'},
        data=json.dumps(booking)
    )

    return result.json()


# add_new_booking(9, 1, 2, '2021-11-09', '10:00:00')
get_availability_by_stylist_by_date(1, '2023-11-01')
