from flask import Flask, jsonify, request #  imports specific objects and functions from the Flask web framework
from db_utils import get_stylist_schedule, add_new_customer, add_new_booking, cancel_booking # imports two specific functions from a module db_utils


# Define a Flask web application
app = Flask(__name__)


# Getting information about stylist appointments for the day
# Define a route to retrieve stylist schedule for a specific date
@app.route('/schedule/<stylist_id>/<date>')
# Calls the 'get_stylist_schedule' function with parameters stylist_id and date
# that returns result as a JSON response
def get_schedule(stylist_id, date):
    res = get_stylist_schedule(stylist_id, date)
    return jsonify(res)

# Creating a new client in a database
# Define a route to add a new client to the database
@app.route('/add_new_client', methods=['POST'])
def add_client():
    # Accepts POST requests with JSON data containing client information
    client = request.get_json()
    # Calls  the 'add_new_customer' function with client information and retrieves the new client's ID
    # and returns created client's ID as a JSON response
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
    
# Cancelling an appointment
@app.route('/cancel_booking/<booking_id>', methods=['DELETE'])  
def cancel_appt(booking_id):
    result = cancel_booking(booking_id)

    return result


if __name__ == '__main__':
    app.run(debug=True)
