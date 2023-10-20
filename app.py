from flask import Flask, jsonify, request
from db_utils import get_stylist_availability, add_booking

app = Flask(__name__)


@app.route('/availability/<stylist>/<date>', methods=['GET'])
def get_booking(stylist, date):
    result = get_stylist_availability(stylist, date)
    return jsonify(result)

#http://127.0.0.1:5001/availability/1/2023-11-01

@app.route('/booking', methods=['POST'])
def book_appt():
    booking = request.get_json()
    booking_id = add_booking(
        customer_id=booking['customer_id'],
        stylist_id=booking['stylist_id'],
        treatment_id=booking['treatment_id'],
        booking_date=booking['booking_date'],
        booking_time=booking['booking_time']
    )
    return jsonify(booking_id)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
