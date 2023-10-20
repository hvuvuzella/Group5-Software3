from flask import Flask, jsonify, request
from db_utils import get_stylist_schedule, add_new_customer, add_new_booking

app = Flask(__name__)


# Getting information about stylist appointments for the day

@app.route('/schedule/<stylist_id>/<date>')
def get_schedule(stylist_id, date):
    res = get_stylist_schedule(stylist_id, date)
    return jsonify(res)

# Creating a new user in a database

@app.route('/add_new_client', methods=['POST'])
def add_client():
    client = request.get_json()
    client_id = add_new_customer(
        first_name=client['first_name'],
        last_name=client['last_name'],
        mobile=client['mobile'],
        email=client['email'],
    )

    return jsonify(client_id)


# Creating a new appointment
@app.route('/add_new_booking', methods=['POST'])
def add_appt():
    booking = request.get_json()
    booking_id = add_new_booking(
        customer_id=booking['customer_id'],
        stylist_id=booking['stylist_id'],
        treatment_id=booking['treatment_id'],
        booking_date=booking['booking_date'],
        booking_time=booking['booking_time']
    )

    return jsonify(booking_id)


if __name__ == '__main__':
    app.run(debug=True)
